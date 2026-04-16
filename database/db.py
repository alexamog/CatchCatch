"""
database/db.py
--------------
Shared data-access layer for CatchCatch.

All JSON file reads and writes go through this module so that the rest of
the codebase never touches file paths or handles I/O errors directly.
"""

import json

CHARACTER_DB = 'database/character_db.json'
USER_DB = 'database/user_db.json'


def load_characters() -> dict:
    """Load and return the full character database.

    Returns a dict of the form ``{'characters': [...]}``.
    Falls back to an empty character list if the file is missing or corrupt.
    """
    try:
        with open(CHARACTER_DB) as fp:
            return json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'characters': []}


def save_characters(data: dict) -> None:
    """Persist the character database to disk.

    Args:
        data: Dict of the form ``{'characters': [...]}`` to write.
    """
    with open(CHARACTER_DB, 'w') as fp:
        json.dump(data, fp, indent=2)


def load_users() -> list:
    """Load and return the list of registered user IDs.

    Falls back to an empty list if the file is missing or corrupt.
    """
    try:
        with open(USER_DB) as fp:
            return json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(data: list) -> None:
    """Persist the user ID list to disk.

    Args:
        data: List of Discord user IDs to write.
    """
    with open(USER_DB, 'w') as fp:
        json.dump(data, fp, indent=2)
