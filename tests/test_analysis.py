import os

os.environ["DATA_CONNECTOR"] = "alpaca"
import asyncio

import pytest
import pytest_asyncio

from liualgotrader.analytics import analysis
from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection


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
@pytest.mark.devtest
async def test_returns() -> None:
    td = await analysis.calc_batch_returns(
        "0664dc2c-f126-4c7f-a069-c5dc246e2df4"
    )
    print(td)
    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_load_trades_by_portfolio():
    trades = await analysis.load_trades_by_portfolio(
        "71f0eaa7-281a-40ad-b120-d2f74eb0b05d"
    )
    print(trades)

    return
