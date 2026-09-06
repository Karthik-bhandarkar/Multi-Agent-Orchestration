import time
import pytest
from src.core.lru_cache import LRUCache


class TestLRUCacheBasics:
    def test_put_and_get(self):
        cache = LRUCache(capacity=3)
        cache.put("x", 100)
        assert cache.get("x") == 100

    def test_missing_key_returns_none(self):
        cache = LRUCache(capacity=3)
        assert cache.get("nonexistent") is None

    def test_update_existing_key(self):
        cache = LRUCache(capacity=3)
        cache.put("x", 1)
        cache.put("x", 2)
        assert cache.get("x") == 2
        assert len(cache) == 1


class TestLRUEviction:
    def test_evicts_least_recently_used(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_get_promotes_to_mru(self):
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3

    def test_capacity_one(self):
        cache = LRUCache(capacity=1)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("a") is None
        assert cache.get("b") == 2

    def test_invalid_capacity_raises(self):
        with pytest.raises(ValueError):
            LRUCache(capacity=0)


class TestLRUPerformance:
    def test_o1_benchmark(self):
        cache = LRUCache(capacity=1000)
        start = time.perf_counter()
        for i in range(1000):
            cache.put(i, i * 2)
        for i in range(1000):
            cache.get(i)
        elapsed_ms = (time.perf_counter() - start) * 1000
        avg_per_op_ms = elapsed_ms / 2000
        print(f"\n[BENCHMARK] LRU avg per-op time: {avg_per_op_ms:.5f} ms")
        assert avg_per_op_ms < 0.05
