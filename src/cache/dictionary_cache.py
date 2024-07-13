from .cache import Cache, CacheEntry
from typing import Dict
from time import time


class DictionaryCache(Cache):
    """A simple dictionary-based Cache implementation that can be initialized
    and used in tests.
    """
    def __init__(self, base_dictionary: Dict[str, CacheEntry] = {}) -> None:
        """Create a new dictionary-based Cache with the provided pre-initialized
        values.

        Args:
            base_dictionary (Dict[str, CacheEntry], optional): Any values to be
            pre-initialized in the cache. Defaults to {}.
        """
        self._dict = base_dictionary

    def get(self, key: str) -> CacheEntry | None:
        """Get a value from the cache. Returns the ``CacheEntry`` or ``None`` if
        the key is not set.

        Args:
            key (str): The key to retrieve.

        Returns:
            CacheEntry | None: The CacheEntry, or None if not yet set.
        """
        if key in self._dict:
            return self._dict[key]
        return None

    def set(self, key: str, value: str) -> None:
        """Set the specified key in the cache to the value provided.

        Args:
            key (str): The key to set.
            value (str): The value to set the key to.
        """
        cache_entry: CacheEntry = {
            "value": value,
            "updated": int(time()),
        }
        self._dict[key] = cache_entry
