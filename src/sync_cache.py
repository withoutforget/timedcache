from dataclasses import dataclass, field
from time import time
from typing import Optional


@dataclass(slots=True, kw_only=True)
class TimedCacheObject[T]:
    object: T = None
    expire_time: int

@dataclass(slots=True)
class TimedCache[T]:
    """
    A container for expiring object.
    Not a thread-safe.

    Get function raises an exception if key doesn't exist / expired.
    Operator[] returns None, if key doesn't exist / expired.
    """

    _data: dict[str, TimedCacheObject[T]] = field(default_factory=dict)
    default_timeout: float = 0.5

    def _create_tco(self, obj: T, timeout: float | None = None) -> TimedCacheObject[T]:
        if timeout is None:
            timeout = self.default_timeout
        return TimedCacheObject[T](object=obj, expire_time=timeout + time())
    
    def _expire_key(self, key: str):
        if key in self._data and self._data[key].expire_time <= time():
            del self._data[key]

    def _get(self, key: str) -> TimedCacheObject:
        self._expire_key(key)
        if key not in self._data:
            raise KeyError("Key doesn't exist")
        return self._data[key]

    def _expire(self):
        for k in self._data.keys():
            self._expire_key(k)

    def _update(self):
        self._expire()

    def append(self, key: str, object: T, timeout: float | None = None):
        self._data[key] = self._create_tco(object, timeout)

    def get(self, key: str) -> T:
        res = self._get(key)
        if res is None:
            raise KeyError("Key is expired")
        return res.object

    def __getitem__(self, key: str) -> T:
        return self.get(key)

    def __setitem__(self, key: str, obj: T):
        return self.append(key, obj)

    def __delitem__(self, key: str):
        del self._data[key]

    def __len__(self) -> int:
        self._update()
        return len(self._data)

    def clear(self):
        self._data.clear()
