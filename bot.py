#!/usr/bin/env python3
"""
YG Gentleman Bot
================
A Telegram bot that gently corrects YN (peasant) phrases to YG (gentleman) language.

Features:
- 30% random trigger rate (configurable)
- Rotating response styles
- User cooldowns (10 min default)
- Phrase cooldowns (30 min default)
- Opt-out system
- Gentleman score tracking
"""

import logging
import random
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

from config import Config, Messages
from vocabulary import VOCABULARY, get_correction
from styles import get_random_response, list_styles
from database import get_db, GentlemanDB

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ===== MESSAGE HANDLER =====

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and check for YN phrases."""
    # Ignore non-message updates
    if not update.message or not update.message.text:
        return

    # Ignore private chats (only work in groups)
    if update.message.chat.type == "private":
        return

    message = update.message
    text = message.text
    user = message.from_user
    chat = message.chat

    db = get_db()

    # Check if bot is enabled for this group
    if not db.is_group_enabled(chat.id):
        return

    # Check if user has opted out
    if db.is_opted_out(user.id):
        return

    # Check for YN phrase
    result = get_correction(text)
    if not result:
        return

    yn_phrase, yg_correction = result

    # Get group settings
    settings = db.get_group_settings(chat.id)
    trigger_rate = settings.get("trigger_rate", Config.DEFAULT_TRIGGER_RATE)
    user_cooldown = settings.get("user_cooldown", Config.USER_COOLDOWN)
    phrase_cooldown = settings.get("phrase_cooldown", Config.PHRASE_COOLDOWN)

    # Check user cooldown
    if db.is_user_on_cooldown(user.id, user_cooldown):
        logger.debug(f"User {user.id} on cooldown, skipping")
        return

    # Check phrase cooldown for this group
    if db.is_phrase_on_cooldown(chat.id, yn_phrase, phrase_cooldown):
        logger.debug(f"Phrase '{yn_phrase}' on cooldown in chat {chat.id}, skipping")
        return

    # 30% random trigger (or configured rate)
    if random.random() > trigger_rate:
        logger.debug(f"Random roll failed ({trigger_rate*100}% chance), skipping")
        return

    # All checks passed - send correction!
    try:
        # Ensure user exists in database
        db.create_or_update_user(user.id, user.username, user.first_name)

        # Get random response
        response = get_random_response(
            yg_correction,
            use_special=Config.ENABLE_SPECIAL_RESPONSES
        )

        # Reply to the message
        await message.reply_text(response)

        # Update cooldowns and stats
        db.update_user_correction(user.id)
        db.update_phrase_cooldown(chat.id, yn_phrase)

        # Log correction
        if Config.ENABLE_LOGGING:
            db.log_correction(user.id, chat.id, yn_phrase, yg_correction)

        logger.info(f"Corrected '{yn_phrase}' -> '{yg_correction}' for user {user.id} in chat {chat.id}")

    except Exception as e:
        logger.error(f"Error sending correction: {e}")


# ===== COMMAND HANDLERS =====

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        "Good evening, distinguished sir.\n\n"
        "I am the YG Gentleman Bot, here to guide your transformation "
        "from YN peasant to refined Young Gentleman.\n\n"
        "Add me to your group and I shall gently correct ungentlemanly speech.\n\n"
        "Use /help for commands."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(Messages.HELP_MESSAGE)


async def cmd_gentleman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /gentleman command - show user's gentleman score."""
    user = update.message.from_user
    db = get_db()

    stats = db.get_user_stats(user.id)
    score = stats["gentleman_score"]

    # Determine encouragement based on score
    if score >= 90:
        encouragement = Messages.SCORE_EXCELLENT
        status = "Distinguished Gentleman"
    elif score >= 70:
        encouragement = Messages.SCORE_GOOD
        status = "Aspiring Gentleman"
    elif score >= 50:
        encouragement = Messages.SCORE_IMPROVING
        status = "Gentleman in Training"
    else:
        encouragement = Messages.SCORE_NEEDS_WORK
        status = "YN in Transformation"

    response = Messages.STATS_TEMPLATE.format(
        score=score,
        corrections=stats["total_corrections"],
        status=status,
        encouragement=encouragement
    )

    await update.message.reply_text(response)


async def cmd_optout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /optout command."""
    user = update.message.from_user
    db = get_db()

    if db.is_opted_out(user.id):
        await update.message.reply_text(Messages.ALREADY_OPTED_OUT)
        return

    db.set_opt_out(user.id, True)
    await update.message.reply_text(Messages.OPT_OUT_SUCCESS)


async def cmd_optin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /optin command."""
    user = update.message.from_user
    db = get_db()

    if not db.is_opted_out(user.id):
        await update.message.reply_text(Messages.ALREADY_OPTED_IN)
        return

    db.set_opt_out(user.id, False)
    await update.message.reply_text(Messages.OPT_IN_SUCCESS)


async def cmd_vocabulary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /vocabulary command - show phrase dictionary."""
    # Split into chunks to avoid message length limits
    vocab_items = list(VOCABULARY.items())

    # Send header
    await update.message.reply_text(Messages.VOCABULARY_HEADER)

    # Send in chunks of 20
    chunk_size = 20
    for i in range(0, len(vocab_items), chunk_size):
        chunk = vocab_items[i:i + chunk_size]
        text = "\n".join(f'"{yn}" -> "{yg}"' for yn, yg in chunk)
        await update.message.reply_text(text)


# ===== ADMIN COMMANDS =====

def is_admin(user_id: int, chat_admins: list = None) -> bool:
    """Check if user is an admin."""
    # Check global admin list
    if user_id in Config.ADMIN_IDS:
        return True
    # Check chat admins if provided
    if chat_admins:
        return any(admin.user.id == user_id for admin in chat_admins)
    return False


async def cmd_setrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setrate command - set trigger rate for this group."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    # Check admin status
    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may adjust settings.")
        return

    # Parse rate argument
    if not context.args:
        db = get_db()
        settings = db.get_group_settings(update.message.chat.id)
        current_rate = settings.get("trigger_rate", Config.DEFAULT_TRIGGER_RATE) * 100
        await update.message.reply_text(f"Current trigger rate: {current_rate:.0f}%\nUsage: /setrate [0-100]")
        return

    try:
        rate = int(context.args[0])
        if not 0 <= rate <= 100:
            raise ValueError("Rate must be 0-100")

        db = get_db()
        db.update_group_settings(update.message.chat.id, trigger_rate=rate / 100)
        await update.message.reply_text(f"Trigger rate set to {rate}%")

    except ValueError as e:
        await update.message.reply_text(f"Invalid rate. Please use a number from 0 to 100.")


async def cmd_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pause command - disable bot in this group."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may pause the bot.")
        return

    db = get_db()
    db.update_group_settings(update.message.chat.id, enabled=False)
    await update.message.reply_text("Gentleman training has been paused in this group.")


async def cmd_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resume command - re-enable bot in this group."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may resume the bot.")
        return

    db = get_db()
    db.update_group_settings(update.message.chat.id, enabled=True)
    await update.message.reply_text("Gentleman training has resumed. The refinement continues!")


async def cmd_resetcooldown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /resetcooldown command - reset all cooldowns for testing."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may reset cooldowns.")
        return

    db = get_db()
    db.reset_all_cooldowns(update.message.chat.id)
    await update.message.reply_text("All cooldowns have been reset. Test away, distinguished sir!")


async def cmd_setcooldown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setcooldown command - set cooldown times."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may adjust cooldowns.")
        return

    db = get_db()
    settings = db.get_group_settings(update.message.chat.id)

    # Show current settings if no args
    if not context.args:
        user_cd = settings.get("user_cooldown", Config.USER_COOLDOWN)
        phrase_cd = settings.get("phrase_cooldown", Config.PHRASE_COOLDOWN)
        await update.message.reply_text(
            f"Current cooldowns:\n"
            f"• User: {user_cd}s ({user_cd//60}min)\n"
            f"• Phrase: {phrase_cd}s ({phrase_cd//60}min)\n\n"
            f"Usage:\n"
            f"/setcooldown user 0 - Disable user cooldown\n"
            f"/setcooldown phrase 0 - Disable phrase cooldown\n"
            f"/setcooldown both 0 - Disable all cooldowns"
        )
        return

    try:
        cooldown_type = context.args[0].lower()
        value = int(context.args[1]) if len(context.args) > 1 else 0

        if cooldown_type == "user":
            db.update_group_settings(update.message.chat.id, user_cooldown=value)
            await update.message.reply_text(f"User cooldown set to {value}s ({value//60}min)")
        elif cooldown_type == "phrase":
            db.update_group_settings(update.message.chat.id, phrase_cooldown=value)
            await update.message.reply_text(f"Phrase cooldown set to {value}s ({value//60}min)")
        elif cooldown_type == "both":
            db.update_group_settings(update.message.chat.id, user_cooldown=value, phrase_cooldown=value)
            await update.message.reply_text(f"All cooldowns set to {value}s ({value//60}min)")
        else:
            await update.message.reply_text("Usage: /setcooldown [user|phrase|both] [seconds]")

    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /setcooldown [user|phrase|both] [seconds]")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - show group statistics."""
    if update.message.chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    chat_admins = await update.message.chat.get_administrators()
    if not is_admin(update.message.from_user.id, chat_admins):
        await update.message.reply_text("Only administrators may view statistics.")
        return

    db = get_db()
    stats = db.get_group_stats(update.message.chat.id)
    settings = db.get_group_settings(update.message.chat.id)

    response = f"""
Group Statistics:

Total Corrections: {stats['total_corrections']}
Trigger Rate: {settings.get('trigger_rate', Config.DEFAULT_TRIGGER_RATE) * 100:.0f}%
Bot Status: {'Enabled' if settings.get('enabled', True) else 'Paused'}

Most Common YN Phrases:
"""
    for phrase, count in stats['top_phrases'][:5]:
        response += f"  - \"{phrase}\": {count} times\n"

    await update.message.reply_text(response)


# ===== ERROR HANDLER =====

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Exception while handling an update: {context.error}")


# ===== MAIN =====

def main():
    """Start the bot."""
    # Validate configuration
    Config.validate()

    # Create application
    app = Application.builder().token(Config.BOT_TOKEN).build()

    # Add handlers
    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("gentleman", cmd_gentleman))
    app.add_handler(CommandHandler("optout", cmd_optout))
    app.add_handler(CommandHandler("optin", cmd_optin))
    app.add_handler(CommandHandler("vocabulary", cmd_vocabulary))

    # Admin commands
    app.add_handler(CommandHandler("setrate", cmd_setrate))
    app.add_handler(CommandHandler("pause", cmd_pause))
    app.add_handler(CommandHandler("resume", cmd_resume))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("resetcooldown", cmd_resetcooldown))
    app.add_handler(CommandHandler("setcooldown", cmd_setcooldown))

    # Message handler (must be last)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    ))

    # Error handler
    app.add_error_handler(error_handler)

    # Start polling
    logger.info(f"Starting {Config.BOT_NAME}...")
    logger.info(f"Trigger rate: {Config.DEFAULT_TRIGGER_RATE * 100}%")
    logger.info(f"User cooldown: {Config.USER_COOLDOWN}s")
    logger.info(f"Phrase cooldown: {Config.PHRASE_COOLDOWN}s")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
