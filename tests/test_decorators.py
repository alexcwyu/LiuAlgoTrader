import asyncio
from datetime import date

import pandas as pd
import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.common.decorators import timeit
from liualgotrader.trading.trader_factory import trader_factory


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


async def reconnect_trader():
    trader = trader_factory()
    return await trader.reconnect()


@timeit
async def get_trading_days(trader, start_date):
    return trader.get_trading_days(start_date)


@pytest.mark.devtest
@pytest.mark.asyncio
async def test_trader_calendar() -> None:
    trader = trader_factory()

    td = await get_trading_days(
        trader=trader, start_date=date(year=2021, month=1, day=1)
    )
    print(td)
    return
