from src import TimedCache, AsyncTimedCache
import pytest

from tests.timers import precise_sync_timer, precise_async_timer

@precise_sync_timer(number = 10_000, repeat = 10)
def test_sync_add_delete():
    """Тестирует синхронное добавление и удаление значения из TimedCache."""
    cache = TimedCache[int](default_timeout=1)
    key = "test_key"
    value = 123
    cache.append(key, value)
    assert cache[key] == value
    del cache._data[key]  # Прямое удаление для теста
    with pytest.raises(KeyError):
        _ = cache[key]

@precise_async_timer(number = 10_000, repeat = 10)
async def test_async_add_delete():
    """Тестирует асинхронное добавление и удаление значения из AsyncTimedCache."""
    cache = AsyncTimedCache[int](cache=TimedCache[int](default_timeout=1))
    key = "test_key"
    value = 456
    await cache.append(key, value)
    assert await cache[key] == value
    del cache._cache._data[key]  # Прямое удаление для теста
    with pytest.raises(KeyError):
        await cache[key]