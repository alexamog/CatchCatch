"""
database/db.py
--------------
SQLite data-access layer for CatchCatch.

All database interaction goes through this module. The SQLite file is
created automatically at database/catchcatch.db on first run via
:func:`init_db`, which must be called once at bot startup.

Schema
------
users(user_id)
characters(id, name, value, owned, owner_id)
"""

import sqlite3
from contextlib import contextmanager

DB_PATH = 'database/catchcatch.db'


@contextmanager
def _connect():
    """Open a connection, commit on success, roll back on error, then close.

    Yields:
        sqlite3.Connection: An open connection with Row factory enabled so
            columns can be accessed by name (e.g. ``row['name']``).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Initialisation ────────────────────────────────────────────────────────────

def init_db() -> None:
    """Create the database tables if they do not already exist.

    Safe to call on every startup — uses ``CREATE TABLE IF NOT EXISTS``
    so existing data is never affected. Also applies any lightweight
    migrations (e.g. adding new columns) that are safe to run repeatedly.
    """
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id  INTEGER PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS characters (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    UNIQUE NOT NULL,
                value     INTEGER NOT NULL,
                owned     INTEGER NOT NULL DEFAULT 0,
                owner_id  INTEGER DEFAULT NULL,
                image_url TEXT    DEFAULT NULL
            );
        """)
        # Migration: add image_url to databases created before this column existed
        try:
            conn.execute('ALTER TABLE characters ADD COLUMN image_url TEXT DEFAULT NULL')
        except Exception:
            pass  # Column already exists


def seed_characters() -> None:
    """Populate the characters table with the default roster.

    Only runs when the table is completely empty, so it will never
    overwrite data added by admins after first launch.

    Rarity tiers
    ------------
    Common     (value  10) — plentiful, easy to get
    Uncommon   (value  50) — moderate chance
    Rare       (value 200) — harder to land
    Epic       (value 500) — very scarce
    Legendary  (value 2000) — extremely rare
    """
    with _connect() as conn:
        count = conn.execute('SELECT COUNT(*) FROM characters').fetchone()[0]
        if count > 0:
            return
        roster = [
            # Common
            ('Goblin',      10),
            ('Slime',       10),
            ('Rat',         10),
            ('Bat',         10),
            ('Wolf',        10),
            ('Sprite',      10),
            ('Imp',         10),
            ('Pixie',       10),
            # Uncommon
            ('Kobold',      50),
            ('Fairy',       50),
            ('Gnome',       50),
            ('Bandit',      50),
            ('Archer',      50),
            ('Scout',       50),
            ('Bard',        50),
            # Rare
            ('Wizard',     200),
            ('Knight',     200),
            ('Paladin',    200),
            ('Rogue',      200),
            ('Ranger',     200),
            ('Monk',       200),
            ('Druid',      200),
            # Epic
            ('Dragon',     500),
            ('Phoenix',    500),
            ('Hydra',      500),
            ('Gryphon',    500),
            ('Titan',      500),
            ('Kraken',     500),
            # Legendary
            ('Celestia',  2000),
            ('Aether',    2000),
            ('Shadowlord', 2000),
        ]
        conn.executemany(
            'INSERT INTO characters (name, value) VALUES (?, ?)', roster
        )


# ── Users ─────────────────────────────────────────────────────────────────────

def is_registered(user_id: int) -> bool:
    """Return True if the given Discord user ID is in the players table.

    Args:
        user_id: Discord user snowflake ID to check.
    """
    with _connect() as conn:
        row = conn.execute(
            'SELECT 1 FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()
        return row is not None


def register_user(user_id: int) -> None:
    """Add a Discord user ID to the players table.

    Uses ``INSERT OR IGNORE`` so calling this for an already-registered
    user is safe and produces no error.

    Args:
        user_id: Discord user snowflake ID to register.
    """
    with _connect() as conn:
        conn.execute(
            'INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,)
        )


# ── Characters ────────────────────────────────────────────────────────────────

def get_character(name: str) -> sqlite3.Row | None:
    """Fetch a single character row by name, or None if not found.

    Args:
        name: Exact character name to look up.

    Returns:
        A ``sqlite3.Row`` with columns ``id``, ``name``, ``value``,
        ``owned``, and ``owner_id``, or ``None`` if no match.
    """
    with _connect() as conn:
        return conn.execute(
            'SELECT * FROM characters WHERE name = ?', (name,)
        ).fetchone()


def character_exists(name: str) -> bool:
    """Return True if a character with the given name already exists.

    Args:
        name: Character name to check.
    """
    return get_character(name) is not None


def get_available_characters() -> list:
    """Return all characters that are not currently owned.

    Returns:
        List of ``sqlite3.Row`` objects ordered by name.
    """
    with _connect() as conn:
        return conn.execute(
            'SELECT * FROM characters WHERE owned = 0 ORDER BY name'
        ).fetchall()


def get_player_characters(user_id: int) -> list:
    """Return all characters owned by a specific player.

    Args:
        user_id: Discord user snowflake ID of the player.

    Returns:
        List of ``sqlite3.Row`` objects ordered by name.
    """
    with _connect() as conn:
        return conn.execute(
            'SELECT * FROM characters WHERE owner_id = ? ORDER BY name',
            (user_id,)
        ).fetchall()


def create_character(name: str, value: int, image_url: str | None = None) -> None:
    """Insert a new character into the pool.

    Args:
        name: Display name for the character (must be unique).
        value: Point value assigned to this character.
        image_url: Optional URL to an image shown in Discord embeds.

    Raises:
        sqlite3.IntegrityError: If a character with this name already exists.
    """
    with _connect() as conn:
        conn.execute(
            'INSERT INTO characters (name, value, image_url) VALUES (?, ?, ?)',
            (name, value, image_url)
        )


def claim_character(name: str, user_id: int) -> None:
    """Mark a character as owned by a player.

    Args:
        name: Name of the character to claim.
        user_id: Discord user snowflake ID of the new owner.
    """
    with _connect() as conn:
        conn.execute(
            'UPDATE characters SET owned = 1, owner_id = ? WHERE name = ?',
            (user_id, name)
        )


def discard_character(name: str, user_id: int) -> bool:
    """Return a character to the pool if the given player owns it.

    Args:
        name: Name of the character to discard.
        user_id: Discord user snowflake ID — must match the current owner.

    Returns:
        True if the character was discarded, False if the player does not
        own that character (no rows were updated).
    """
    with _connect() as conn:
        cursor = conn.execute(
            'UPDATE characters SET owned = 0, owner_id = NULL '
            'WHERE name = ? AND owner_id = ?',
            (name, user_id)
        )
        return cursor.rowcount > 0
