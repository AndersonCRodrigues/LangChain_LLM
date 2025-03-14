import hashlib
import json
import os


class SimpleDiskCache:
    def __init__(self, cache_dir="cache_dir"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key):
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.json")

    def lookup(self, key, llm_string):
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    def update(self, key, value, llm_string):
        cache_path = self._get_cache_path(key)
        with open(cache_path, "w") as f:
            json.dump(value, f)
