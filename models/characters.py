"""
models/characters.py
--------------------
Defines the Character data model used throughout CatchCatch.
"""


class Character:
    """Represents a collectible character in the gacha pool.

    Attributes:
        name: The character's display name.
        value: Point value assigned to this character.
        owned: Whether the character is currently owned by a player.
    """

    def __init__(self, name: str, value: int, owned: bool = False, owner: int | None = None) -> None:
        """Initialise a Character.

        Args:
            name: The character's display name.
            value: Point value for this character.
            owned: Whether the character starts as owned. Defaults to False.
            owner: Discord user ID of the owner, or None if unowned.
        """
        self.name = name
        self.value = int(value)
        self.owned = owned
        self._owner = owner

    def discard(self) -> None:
        """Return the character to the pool by clearing its owner."""
        self._owner = None
        self.owned = False

    @property
    def owner(self) -> int | None:
        """Discord user ID of the current owner, or None if unowned."""
        return self._owner

    def to_dict(self) -> dict:
        """Serialise the character to a JSON-compatible dict.

        Returns:
            A dict matching the schema used in character_db.json.
        """
        return {
            'character_name': self.name,
            'character_value': self.value,
            'owned': self.owned,
            'owner_id': self._owner,
        }
