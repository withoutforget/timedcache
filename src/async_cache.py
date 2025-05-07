from src.sync_cache import TimedCache
from typing import Optional, Protocol
from types import TracebackType
from threading import Lock
from dataclasses import dataclass, field

@dataclass(slots=True)
class AsyncTimedCache[T]:
    """
    Thread-safe version of timed-cache. Pseudo-async
    """

    cache: TimedCache[T] = field(default_factory=TimedCache[T])
    mutex: Lock = field(default_factory=Lock)



    async def append(self, key: str, object: T, timeout: float | None = None):
        with self.mutex:
            return self.cache.append(key=key, object=object, timeout=timeout)

    async def get(self, key: str) -> T:
        with self.mutex:
            return self.cache.get(key)

    async def __getitem__(self, key: str) -> T:
        with self.mutex:
            return self.cache[key]

    def __setitem__(self, key: str, obj: T):
        with self.mutex:
            self.cache[key] = obj

    def __delitem__(self, key: str):
        with self.mutex:
            del self.cache[key]

    def __len__(self):
        with self.mutex:
            return len(self.cache)
