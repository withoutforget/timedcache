from dataclasses import dataclass
from time import time
from typing import Optional


@dataclass(slots=True, kw_only=True)
class TimedCacheObject[T]:
    object: Optional[T] = None
    expire_time: int


class TimedCache[T]:
    """
    A container for expiring object.
    Not a thread-safe.

    Get function raises an exception if key doesn't exist / expired.
    Operator[] returns None, if key doesn't exist / expired.
    """

    _data: dict[str, TimedCacheObject[T]] = dict()
    _default_timeout: Optional[float] = None

    def _create_tco(self, obj: T, timeout: float | None = None) -> TimedCacheObject[T]:
        if timeout is None:
            if self._default_timeout is None:
                raise RuntimeError("No timeout to use")
            timeout = self._default_timeout
        return TimedCacheObject[T](object=obj, expire_time=timeout + time())

    def _get(self, key: str) -> Optional[TimedCacheObject]:
        if key in self._data:
            res = self._data[key]
            if res.expire_time >= time():
                return self._data[key]
            del self._data[key]

    def _expire(self):
        curr = time()
        for k, v in self._data.items():
            if v.expire_time <= curr:
                del self._data[k]

    def _update(self):
        self._expire()

    def __init__(self, default_timeout: float | None = None):
        self._default_timeout = default_timeout

    def append(self, key: str, object: T, timeout: float | None = None):
        self._data[key] = self._create_tco(object, timeout)

    def get(self, key: str) -> T:
        res = self._get(key)
        if res is None:
            raise KeyError("Key is expired")
        return res.object

    def __getitem__(self, key: str) -> Optional[T]:
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
