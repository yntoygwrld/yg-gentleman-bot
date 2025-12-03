"""
Database Handler
================
SQLite database for tracking user cooldowns, correction counts, and opt-outs.
"""

import sqlite3
import time
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Default database path
DB_PATH = Path(__file__).parent / "data" / "gentleman.db"


class GentlemanDB:
    """SQLite database handler for the YG Gentleman Bot."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # User data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_correction_time REAL DEFAULT 0,
                    total_corrections INTEGER DEFAULT 0,
                    opted_out INTEGER DEFAULT 0,
                    created_at REAL DEFAULT (strftime('%s', 'now')),
                    updated_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)

            # Phrase cooldowns table (per-group)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phrase_cooldowns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    phrase TEXT,
                    last_used_time REAL,
                    UNIQUE(chat_id, phrase)
                )
            """)

            # Group settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS group_settings (
                    chat_id INTEGER PRIMARY KEY,
                    chat_title TEXT,
                    trigger_rate REAL DEFAULT 0.30,
                    user_cooldown INTEGER DEFAULT 600,
                    phrase_cooldown INTEGER DEFAULT 1800,
                    enabled INTEGER DEFAULT 1,
                    created_at REAL DEFAULT (strftime('%s', 'now')),
                    updated_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)

            # Correction history (for analytics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS corrections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    yn_phrase TEXT,
                    yg_correction TEXT,
                    timestamp REAL DEFAULT (strftime('%s', 'now'))
                )
            """)

            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    # ===== USER METHODS =====

    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user data by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
        return None

    def create_or_update_user(self, user_id: int, username: str = None, first_name: str = None):
        """Create or update user record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = COALESCE(excluded.username, username),
                    first_name = COALESCE(excluded.first_name, first_name),
                    updated_at = excluded.updated_at
            """, (user_id, username, first_name, time.time()))
            conn.commit()

    def is_user_on_cooldown(self, user_id: int, cooldown_seconds: int = 600) -> bool:
        """Check if user is on correction cooldown."""
        user = self.get_user(user_id)
        if not user:
            return False

        time_since_last = time.time() - user["last_correction_time"]
        return time_since_last < cooldown_seconds

    def update_user_correction(self, user_id: int):
        """Update user's last correction time and increment count."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET last_correction_time = ?,
                    total_corrections = total_corrections + 1,
                    updated_at = ?
                WHERE user_id = ?
            """, (time.time(), time.time(), user_id))
            conn.commit()

    def get_user_stats(self, user_id: int) -> dict:
        """Get user's gentleman statistics."""
        user = self.get_user(user_id)
        if not user:
            return {
                "total_corrections": 0,
                "opted_out": False,
                "gentleman_score": 100,
            }

        # Lower corrections = higher score
        score = max(0, 100 - (user["total_corrections"] * 2))

        return {
            "total_corrections": user["total_corrections"],
            "opted_out": bool(user["opted_out"]),
            "gentleman_score": score,
        }

    def set_opt_out(self, user_id: int, opted_out: bool):
        """Set user's opt-out status."""
        self.create_or_update_user(user_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET opted_out = ?, updated_at = ? WHERE user_id = ?",
                (1 if opted_out else 0, time.time(), user_id)
            )
            conn.commit()

    def is_opted_out(self, user_id: int) -> bool:
        """Check if user has opted out of corrections."""
        user = self.get_user(user_id)
        return user and bool(user["opted_out"])

    # ===== PHRASE COOLDOWN METHODS =====

    def is_phrase_on_cooldown(self, chat_id: int, phrase: str, cooldown_seconds: int = 1800) -> bool:
        """Check if a phrase was recently corrected in this chat."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT last_used_time FROM phrase_cooldowns
                WHERE chat_id = ? AND phrase = ?
            """, (chat_id, phrase.lower()))
            row = cursor.fetchone()

            if not row:
                return False

            time_since_last = time.time() - row[0]
            return time_since_last < cooldown_seconds

    def update_phrase_cooldown(self, chat_id: int, phrase: str):
        """Update the cooldown timestamp for a phrase in a chat."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO phrase_cooldowns (chat_id, phrase, last_used_time)
                VALUES (?, ?, ?)
                ON CONFLICT(chat_id, phrase) DO UPDATE SET
                    last_used_time = excluded.last_used_time
            """, (chat_id, phrase.lower(), time.time()))
            conn.commit()

    # ===== GROUP SETTINGS METHODS =====

    def get_group_settings(self, chat_id: int) -> dict:
        """Get group settings, creating default if not exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM group_settings WHERE chat_id = ?",
                (chat_id,)
            )
            row = cursor.fetchone()

            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))

        # Return defaults if not found
        return {
            "chat_id": chat_id,
            "trigger_rate": 0.30,
            "user_cooldown": 600,
            "phrase_cooldown": 1800,
            "enabled": True,
        }

    def update_group_settings(self, chat_id: int, **kwargs):
        """Update group settings."""
        valid_fields = {"trigger_rate", "user_cooldown", "phrase_cooldown", "enabled", "chat_title"}
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}

        if not updates:
            return

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Insert or update
            cursor.execute("""
                INSERT INTO group_settings (chat_id, chat_title)
                VALUES (?, ?)
                ON CONFLICT(chat_id) DO NOTHING
            """, (chat_id, kwargs.get("chat_title", "")))

            # Build update query
            set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
            values = list(updates.values()) + [time.time(), chat_id]

            cursor.execute(f"""
                UPDATE group_settings
                SET {set_clause}, updated_at = ?
                WHERE chat_id = ?
            """, values)
            conn.commit()

    def is_group_enabled(self, chat_id: int) -> bool:
        """Check if bot is enabled for this group."""
        settings = self.get_group_settings(chat_id)
        return settings.get("enabled", True)

    # ===== CORRECTION HISTORY =====

    def log_correction(self, user_id: int, chat_id: int, yn_phrase: str, yg_correction: str):
        """Log a correction to history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO corrections (user_id, chat_id, yn_phrase, yg_correction)
                VALUES (?, ?, ?, ?)
            """, (user_id, chat_id, yn_phrase, yg_correction))
            conn.commit()

    def get_group_stats(self, chat_id: int) -> dict:
        """Get statistics for a group."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total corrections
            cursor.execute(
                "SELECT COUNT(*) FROM corrections WHERE chat_id = ?",
                (chat_id,)
            )
            total_corrections = cursor.fetchone()[0]

            # Most common phrases
            cursor.execute("""
                SELECT yn_phrase, COUNT(*) as count
                FROM corrections
                WHERE chat_id = ?
                GROUP BY yn_phrase
                ORDER BY count DESC
                LIMIT 5
            """, (chat_id,))
            top_phrases = cursor.fetchall()

            # Most corrected users
            cursor.execute("""
                SELECT user_id, COUNT(*) as count
                FROM corrections
                WHERE chat_id = ?
                GROUP BY user_id
                ORDER BY count DESC
                LIMIT 5
            """, (chat_id,))
            top_users = cursor.fetchall()

            return {
                "total_corrections": total_corrections,
                "top_phrases": top_phrases,
                "top_users": top_users,
            }


# Singleton instance
_db_instance: Optional[GentlemanDB] = None


def get_db() -> GentlemanDB:
    """Get the database singleton instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = GentlemanDB()
    return _db_instance


if __name__ == "__main__":
    # Test the database
    db = get_db()

    # Test user operations
    db.create_or_update_user(123456, "testuser", "Test")
    print(f"User: {db.get_user(123456)}")
    print(f"On cooldown: {db.is_user_on_cooldown(123456)}")

    # Test phrase cooldown
    print(f"Phrase cooldown: {db.is_phrase_on_cooldown(-100, 'bruh')}")
    db.update_phrase_cooldown(-100, "bruh")
    print(f"Phrase cooldown after update: {db.is_phrase_on_cooldown(-100, 'bruh')}")

    # Test group settings
    print(f"Group settings: {db.get_group_settings(-100)}")
