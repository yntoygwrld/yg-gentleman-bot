"""
Configuration Settings
======================
Bot configuration loaded from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Config:
    """Bot configuration settings."""

    # ===== REQUIRED =====
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    # ===== TRIGGER SETTINGS =====
    # Probability of responding to a detected phrase (0.0 to 1.0)
    DEFAULT_TRIGGER_RATE: float = float(os.getenv("TRIGGER_RATE", "0.30"))

    # ===== COOLDOWN SETTINGS =====
    # User cooldown in seconds (default: 10 minutes)
    USER_COOLDOWN: int = int(os.getenv("USER_COOLDOWN", "600"))

    # Phrase cooldown in seconds (default: 30 minutes)
    PHRASE_COOLDOWN: int = int(os.getenv("PHRASE_COOLDOWN", "1800"))

    # Global group cooldown - max corrections per minute
    GROUP_RATE_LIMIT: int = int(os.getenv("GROUP_RATE_LIMIT", "3"))

    # ===== FEATURE TOGGLES =====
    # Enable special responses (YN to YG transformation phrases)
    ENABLE_SPECIAL_RESPONSES: bool = os.getenv("ENABLE_SPECIAL_RESPONSES", "true").lower() == "true"

    # Enable correction logging to database
    ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"

    # Enable user stats tracking
    ENABLE_STATS: bool = os.getenv("ENABLE_STATS", "true").lower() == "true"

    # ===== DATABASE =====
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/gentleman.db")

    # ===== ADMIN SETTINGS =====
    # Comma-separated list of admin user IDs
    ADMIN_IDS: list[int] = [
        int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",")
        if x.strip().isdigit()
    ]

    # ===== BOT INFO =====
    BOT_NAME: str = os.getenv("BOT_NAME", "YG Gentleman Bot")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "")

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required!")
        return True

    @classmethod
    def to_dict(cls) -> dict:
        """Return configuration as dictionary (for debugging)."""
        return {
            "BOT_TOKEN": cls.BOT_TOKEN[:10] + "..." if cls.BOT_TOKEN else None,
            "DEFAULT_TRIGGER_RATE": cls.DEFAULT_TRIGGER_RATE,
            "USER_COOLDOWN": cls.USER_COOLDOWN,
            "PHRASE_COOLDOWN": cls.PHRASE_COOLDOWN,
            "GROUP_RATE_LIMIT": cls.GROUP_RATE_LIMIT,
            "ENABLE_SPECIAL_RESPONSES": cls.ENABLE_SPECIAL_RESPONSES,
            "ENABLE_LOGGING": cls.ENABLE_LOGGING,
            "ENABLE_STATS": cls.ENABLE_STATS,
            "DATABASE_PATH": cls.DATABASE_PATH,
            "ADMIN_IDS": cls.ADMIN_IDS,
            "BOT_NAME": cls.BOT_NAME,
        }


# Messages for the bot
class Messages:
    """Bot response messages."""

    # Opt-out messages
    OPT_OUT_SUCCESS = (
        "Very well, dear sir. You have been excused from etiquette training. "
        "Use /optin should you wish to resume your transformation to gentleman."
    )
    OPT_IN_SUCCESS = (
        "Splendid! Welcome back to the path of refinement. "
        "Your journey from YN to YG continues."
    )
    ALREADY_OPTED_OUT = "You have already opted out, dear sir."
    ALREADY_OPTED_IN = "You are already receiving guidance, good fellow."

    # Stats messages
    STATS_TEMPLATE = """
Your Gentleman Profile:

Gentleman Score: {score}/100
Total Corrections: {corrections}
Status: {status}

{encouragement}
"""

    # Score-based encouragement
    SCORE_EXCELLENT = "Exemplary! You speak like a true YG."
    SCORE_GOOD = "Quite distinguished. The transformation progresses."
    SCORE_IMPROVING = "Progress noted. Continue the refinement."
    SCORE_NEEDS_WORK = "The journey continues. Every correction brings growth."

    # Help message
    HELP_MESSAGE = """
YG Gentleman Bot

Training young gentlemen, one phrase at a time.

Commands:
/gentleman - Check your gentleman score
/optout - Disable corrections for yourself
/optin - Re-enable corrections
/vocabulary - View the YN to YG dictionary
/help - Show this message

Admin Commands:
/setrate [0-100] - Set trigger rate percentage
/pause - Pause corrections in this group
/resume - Resume corrections
/stats - View group statistics
"""

    # Vocabulary header
    VOCABULARY_HEADER = """
The YN to YG Vocabulary

A distinguished gentleman's guide to refined expression:

"""


if __name__ == "__main__":
    # Print configuration for debugging
    print("Current Configuration:")
    for key, value in Config.to_dict().items():
        print(f"  {key}: {value}")
