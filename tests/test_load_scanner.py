import asyncio

import pytest
import pytest_asyncio

from liualgotrader.common.data_loader import DataLoader  # type:ignore
from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.scanners.base import Scanner


@pytest_asyncio.fixture(autouse=True)
async def _initialized_resources():
    await create_db_connection()
    pool = config.db_conn_pool
    try:
        yield
    finally:
        await pool.close()
        if getattr(config, "db_conn_pool", None) is pool:
            del config.db_conn_pool


@pytest.mark.asyncio
async def test_get_scanner():
    dl = DataLoader()
    s = await Scanner.get_scanner(
        data_loader=dl,
        scanner_name="MyScanner",
        scanner_details={
            "filename": "./examples/scanners/my_scanner.py",
        },
    )

    if not s:
        raise AssertionError("Failed to instantiate scanner")

    print(f"Loaded scanner {s.name}")

    return
