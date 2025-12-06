# YG Gentleman Bot (Uncle Cornelius) - Claude Code Instructions

## Project Overview
Telegram bot that gently corrects "YN" (peasant) phrases to "YG" (gentleman) language. Used in $YNTOYG community groups.

## GitHub Account
- **Username:** `yntoygwrld` (NOT relaxshadow!)
- **Repository:** `yntoygwrld/yg-gentleman-bot`
- **Branch:** `main`

### Before Any Git Operations:
1. Verify `git remote -v` shows `yntoygwrld/yg-gentleman-bot`
2. If wrong, fix with: `git remote set-url origin https://github.com/yntoygwrld/yg-gentleman-bot.git`

## Deployment

### Platform: Koyeb
- **Service Name**: `yg-gentleman-bot`
- **GitHub Repo**: `yntoygwrld/yg-gentleman-bot`
- **Procfile**: `worker: python bot.py`

### Environment Variables (Set in Koyeb Dashboard)
```
BOT_TOKEN=<from BotFather>
ADMIN_IDS=8227072324
```

## Admin User
- **Telegram ID**: 8227072324 (@OriginalYG)
- Hardcoded in `config.py` as fallback
- **ONLY the bot owner can use admin commands** - not group admins!

## Admin Commands (Owner Only)
| Command | Description |
|---------|-------------|
| `/setrate [0-100]` | Set trigger rate percentage |
| `/pause` | Pause corrections in group |
| `/resume` | Resume corrections |
| `/stats` | View group statistics |
| `/resetcooldown` | Reset all cooldowns |
| `/setcooldown` | Set cooldown times |
| `/defaults` | Reset to default settings |

## User Commands (Everyone)
| Command | Description |
|---------|-------------|
| `/start` | Introduction message |
| `/help` | Show commands |
| `/gentleman` | Check gentleman score |
| `/optout` | Disable corrections for yourself |
| `/optin` | Re-enable corrections |
| `/vocabulary` | View YN to YG dictionary |

## File Structure
```
bot.py          # Main bot handlers
config.py       # Configuration & admin IDs
database.py     # SQLite operations
vocabulary.py   # YN -> YG phrase mappings
styles.py       # Response style templates
Procfile        # Koyeb worker config
```

---

## MANDATORY: Git Commit & Push & Deploy Protocol

**CRITICAL: After ANY code changes, you MUST commit, push, AND redeploy immediately.**

### Why This Matters
- Local changes DO NOTHING until pushed AND redeployed
- The bot runs on Koyeb, NOT locally
- User expects changes to be live immediately
- Koyeb uses "Public repository" mode - NO auto-deploy!

### After Every Code Change:
```bash
cd /mnt/x/YNTOYG/yg-gentleman-bot
git add -A
git commit -m "descriptive message"
git push origin main
```

### AUTOMATED KOYEB REDEPLOY (Use Playwright!)
After pushing code, use Playwright MCP to trigger redeploy:

1. **Navigate to Koyeb** (if not already open):
   - Use `browser_tabs` to select Koyeb tab, or
   - Use `browser_navigate` to `https://app.koyeb.com/services`

2. **Click on yg-gentleman-bot service**

3. **Click "Redeploy" button**

4. **In dialog, click "Trigger build"** (NOT "Skip build")

5. **Wait ~60 seconds** for deployment

6. **Verify status shows "Healthy"**

**This is MANDATORY after every push - do NOT ask user to do it manually!**

### DO NOT:
- Leave changes uncommitted
- Wait for user to ask you to push
- Assume local changes affect the live bot
- Forget to redeploy on Koyeb after pushing
- Skip the redeploy step

### DO:
- Commit immediately after making changes
- Push to GitHub (`yntoygwrld/yg-gentleman-bot`)
- Write clear commit messages
- Go to Koyeb and click "Redeploy" -> "Trigger build"
- Verify deployment becomes healthy

### Verification After Push + Redeploy:
1. Check git status shows clean working tree
2. Go to Koyeb dashboard -> Services -> yg-gentleman-bot
3. Click "Redeploy" -> "Trigger build"
4. Wait for build to complete (~30-60 seconds)
5. Verify deployment shows "Healthy"

**REMEMBER: Changes only go live after `git push` AND Koyeb redeploy!**
