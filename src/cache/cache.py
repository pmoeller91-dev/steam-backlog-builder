import abc
from typing import TypedDict


class CacheEntry(TypedDict):
    """A very simple cache entry for a key-value cache."""

    value: str
    updated: float


class Cache(metaclass=abc.ABCMeta):
    """A very simple interface for a key-value cache."""

    @abc.abstractmethod
    def get(self, key: str) -> CacheEntry | None:
        """Get the value with the given key.

        Args:
            key (str): The key value to retrieve.

        Returns:
            CacheEntry | None: The CacheEntry associated with the ``key`` or
            ``None`` if it has not been set.
        """
        pass

    @abc.abstractmethod
    def set(self, key: str, value: str) -> None:
        """Set the value with the given key to the provided value.

        Args:
            key (str): The key value to set.
            value (str): The value to set the key to.
        """
        pass
