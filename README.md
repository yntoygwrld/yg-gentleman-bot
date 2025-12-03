# YG Gentleman Bot

A Telegram bot that gently corrects YN (peasant) phrases to YG (gentleman) language. Training young gentlemen, one phrase at a time.

## Features

- **30% Random Trigger** - Only responds to ~30% of detected phrases (configurable)
- **8 Rotating Response Styles** - Butler, Professor, Mentor, Aristocrat, Connoisseur, Elder, Diplomat, Steward
- **100+ Phrase Vocabulary** - Comprehensive YN to YG dictionary
- **Smart Cooldowns** - Prevents spam with user and phrase cooldowns
- **Opt-out System** - Users can disable corrections for themselves
- **Gentleman Score** - Track transformation progress
- **Admin Controls** - Configure per-group settings

## Quick Start

### 1. Create Your Bot with BotFather

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose a name: `YG Gentleman Bot`
4. Choose a username: `YGGentlemanBot` (must be unique, end with "bot")
5. **Save the API token** - you'll need it!

### 2. Install Dependencies

```bash
# Clone/download the bot files
cd yg-gentleman-bot

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Bot

```bash
# Copy the example config
cp .env.example .env

# Edit .env with your bot token
nano .env  # or use any text editor
```

Set at minimum:
```
BOT_TOKEN=your_bot_token_from_botfather
```

### 4. Run the Bot

```bash
python bot.py
```

### 5. Add to Your Group

1. Add your bot to the group
2. Make the bot an admin with these permissions:
   - Read Messages
   - Send Messages
3. The bot will now automatically correct YN phrases!

## Commands

### User Commands
| Command | Description |
|---------|-------------|
| `/start` | Introduction message |
| `/help` | Show all commands |
| `/gentleman` | Check your gentleman score |
| `/optout` | Disable corrections for yourself |
| `/optin` | Re-enable corrections |
| `/vocabulary` | View the YN to YG dictionary |

### Admin Commands
| Command | Description |
|---------|-------------|
| `/setrate [0-100]` | Set trigger rate percentage |
| `/pause` | Temporarily disable bot |
| `/resume` | Re-enable bot |
| `/stats` | View group statistics |

## Configuration Options

All options can be set in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `BOT_TOKEN` | (required) | Telegram bot token |
| `TRIGGER_RATE` | 0.30 | Probability of responding (30%) |
| `USER_COOLDOWN` | 600 | Seconds between corrections per user (10 min) |
| `PHRASE_COOLDOWN` | 1800 | Seconds before same phrase corrected again (30 min) |
| `GROUP_RATE_LIMIT` | 3 | Max corrections per minute per group |
| `ADMIN_IDS` | (empty) | Comma-separated user IDs for global admins |

## Response Styles

The bot rotates through 8 refined response styles:

1. **The Butler** - Warm & welcoming
   > "Ahem, if one may... a gentleman would say: 'Good evening, gentlemen'"

2. **The Professor** - Educational
   > "A note on etiquette, dear sir: 'Indeed' is the preferred phrasing."

3. **The Mentor** - Encouraging
   > "Almost there, good sir. Perhaps try: 'Very well'"

4. **The Aristocrat** - Playful
   > "Good heavens! Might one suggest: 'How extraordinary'"

5. **The Connoisseur** - Refined
   > "A distinguished gentleman would phrase it thus: 'Exquisite'"

6. **The Elder** - Wise
   > "In refined circles, one says: 'Most certainly'"

7. **The Diplomat** - Gracious
   > "Might one offer a suggestion? 'Speaking candidly'"

8. **The Steward** - Helpful
   > "The proper expression, dear fellow: 'Quite so'"

## Vocabulary Highlights

| YN (Peasant) | YG (Gentleman) |
|--------------|----------------|
| "yo what's good" | "Good evening, gentlemen" |
| "lfg" | "The hour of prosperity is upon us" |
| "no cap" | "In all sincerity" |
| "wagmi" | "Together we shall flourish" |
| "bruh" | "Distinguished sir" |
| "fire" | "Exquisite" |
| "rekt" | "Financially inconvenienced" |
| "diamond hands" | "Steadfast conviction" |

See the full 100+ phrase vocabulary with `/vocabulary` command.

## Deployment

### Railway (Recommended - Free Tier)

1. Fork/upload to GitHub
2. Create account at [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
4. Add environment variable: `BOT_TOKEN`
5. Deploy!

### Render (Free Tier)

1. Create account at [render.com](https://render.com)
2. New → Background Worker
3. Connect GitHub repo
4. Add environment variable: `BOT_TOKEN`
5. Deploy!

### Self-Hosted

```bash
# Run with screen/tmux
screen -S gentleman-bot
python bot.py
# Ctrl+A, D to detach

# Or with systemd
sudo nano /etc/systemd/system/gentleman-bot.service
```

Example systemd service:
```ini
[Unit]
Description=YG Gentleman Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/yg-gentleman-bot
Environment=BOT_TOKEN=your_token
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## File Structure

```
yg-gentleman-bot/
├── bot.py              # Main bot logic
├── vocabulary.py       # YN → YG dictionary (100+ phrases)
├── styles.py           # Response templates (8 styles)
├── database.py         # SQLite cooldown/stats tracking
├── config.py           # Configuration loader
├── requirements.txt    # Python dependencies
├── .env.example        # Example configuration
├── .env                # Your configuration (create this)
├── data/
│   └── gentleman.db    # SQLite database (auto-created)
└── README.md           # This file
```

## The YN to YG Transformation

This bot is part of the $YNTOYG memecoin project celebrating the transformation from "Young N****s" to "Young Gentlemen" - a journey from street life to success through crypto investment.

**Key Elements:**
- Quarter-zip sweaters (the hero garment)
- Matcha-sipping lifestyle
- Black excellence refined
- From tracksuits to tailored

---

*Training Young Gentlemen, one phrase at a time.*
