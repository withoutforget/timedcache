from tests.all_tests import test_sync_add_delete, test_async_add_delete
from tests.logging_setup import setup_logging

async def run_tests():
    setup_logging()
    await test_async_add_delete()
    test_sync_add_delete()