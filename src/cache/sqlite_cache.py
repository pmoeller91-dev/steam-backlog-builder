from .cache import Cache, CacheEntry
import sqlite3
from inspect import cleandoc
from time import time
import os


class SQLiteCache(Cache):
    """Creates a cache object which uses the file at ``filePath`` as the SQLite
    database file. If the file does not exist, it will be created. If it does
    exist, the existing information will be used.
    """

    def __init__(self, filePath: str | bytes | os.PathLike) -> None:
        """Create a new SQLiteCache using the specified file as a database.

        Args:
            filePath (str): The file to use for the database.
        """
        parent_dir = os.path.dirname(filePath)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        self._con = sqlite3.connect(filePath)
        self._cur = self._con.cursor()
        self._create_table()

    def __del__(self) -> None:
        """Close connection to the file database."""
        self._con.close()

    def get(self, key: str) -> CacheEntry | None:
        """Get the specified key.

        Args:
            key (str): The key to fetch

        Returns:
            CacheEntry | None: The CacheEntry associated with the key, or None if not set
        """
        res = self._cur.execute(
            cleandoc(
                f"""
                SELECT value, updated FROM cache WHERE key='{key}'
                """
            )
        )
        row: tuple[str, int] | None = res.fetchone()
        if row is None:
            return None
        cache_entry: CacheEntry = {
            "value": row[0],
            "updated": row[1],
        }
        return cache_entry

    def set(self, key: str, value: str) -> None:
        """Set the given key to the provided value.

        Args:
            key (str): The key to set
            value (str): The value to set the key to
        """
        self._cur.execute(
            "REPLACE INTO cache (key, value, updated) VALUES(?, ?, ?)",
            (key, value, int(time())),
        )

    def _create_table(self) -> None:
        """Create the cache table if it does not exist."""
        self._cur.execute(
            cleandoc(
                f"""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated INTEGER DEFAULT 0
                ) WITHOUT ROWID;
                """
            )
        )
