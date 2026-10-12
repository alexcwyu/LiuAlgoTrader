import asyncio
import uuid

import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.strategies.base import Strategy


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
async def test_get_strategy():
    s = await Strategy.get_strategy(
        batch_id=str(uuid.uuid4()),
        strategy_name="MyStrategy",
        strategy_details={
            "filename": "./examples/skeleton-strategy/my_strategy.py",
            "schedule": [],
        },
    )

    if not s:
        raise AssertionError("Failed to instantiate strategy")

    print(f"Loaded strategy {s.name}")

    return
