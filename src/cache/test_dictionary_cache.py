import unittest
from .dictionary_cache import DictionaryCache, CacheEntry


class TestDictionaryCache(unittest.TestCase):

    def test_exists_empty(self):
        cache = DictionaryCache()
        test_key = "some_key"
        expected_value = "some_value"
        cache.set(test_key, expected_value)
        cache_entry = cache.get(test_key)
        assert cache_entry is not None
        self.assertEqual(cache_entry["value"], expected_value)

    def test_exists_populated(self):
        test_key = "some_key"
        expected_value = "some_value"
        expected_updated = 123456789
        initial_values: dict[str, CacheEntry] = {
            test_key: {
                "value": expected_value,
                "updated": expected_updated,
            }
        }
        cache = DictionaryCache(initial_values)
        cache_entry = cache.get(test_key)
        assert cache_entry is not None
        self.assertEqual(cache_entry["value"], expected_value)
        self.assertEqual(cache_entry["updated"], expected_updated)

    def test_does_not_exist(self):
        cache = DictionaryCache()
        test_key = "some_key"
        cache_entry = cache.get(test_key)
        self.assertIs(cache_entry, None)


if __name__ == "__main__":
    unittest.main()
