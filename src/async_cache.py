from src.sync_cache import TimedCache
from typing import Optional
from threading import Lock


class AsyncTimedCache[T]:
    """
    Thread-safe version of timed-cache. Pseudo-async
    """

    _cache: TimedCache[T]
    _mutex: Lock

    def __init__(
        self, mutex: Optional[Lock] = None, cache: TimedCache[T] | None = None
    ):
        if mutex is None:
            mutex = Lock()
        self._mutex = mutex
        if cache is None:
            cache = TimedCache[T]()
        self._cache = cache

    async def append(self, key: str, object: T, timeout: float | None = None):
        with self._mutex:
            return self._cache.append(key=key, object=object, timeout=timeout)

    async def get(self, key: str) -> T:
        with self._mutex:
            return self._cache.get(key)

    async def __getitem__(self, key: str) -> T:
        with self._mutex:
            return self._cache[key]

    def __setitem__(self, key: str, obj: T):
        with self._mutex:
            self._cache[key] = obj

    def __delitem__(self, key: str):
        del self._cache[key]
