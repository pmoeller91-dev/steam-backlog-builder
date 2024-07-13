import unittest
from from_root import from_root
from .sqlite_cache import SQLiteCache

db_path = from_root(".cache", "test_sqlite_cache.db")


class TestSQLiteCache(unittest.TestCase):
    def setUp(self):
        self.cache = SQLiteCache(db_path)

    def tearDown(self) -> None:
        db_path.unlink(missing_ok=True)

    def test_exists(self):
        test_key = "some_key"
        expected_value = "some_value"
        self.cache.set(test_key, expected_value)
        cache_entry = self.cache.get(test_key)
        assert cache_entry is not None
        self.assertEqual(cache_entry["value"], expected_value)

    def test_does_not_exist(self):
        test_key = "some_key"
        cache_entry = self.cache.get(test_key)
        self.assertIs(cache_entry, None)


if __name__ == "__main__":
    unittest.main()
