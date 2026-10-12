import asyncio

import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.trading.alpaca import AlpacaTrader

alpaca_trader: AlpacaTrader


@pytest_asyncio.fixture(autouse=True)
async def _initialized_resources():
    global alpaca_trader
    await create_db_connection()
    pool = config.db_conn_pool
    try:
        alpaca_trader = AlpacaTrader()
        yield
    finally:
        await pool.close()
        if getattr(config, "db_conn_pool", None) is pool:
            del config.db_conn_pool


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_get_symbols():
    global alpaca_trader
    assets = await alpaca_trader.get_tradeable_symbols()
    print(assets)
    print(len(assets))
    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_get_shortable_symbols():
    global alpaca_trader
    assets = await alpaca_trader.get_shortable_symbols()
    print(assets)
    print(len(assets))
    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_is_fractionable():
    global alpaca_trader
    apa_fractionable = await alpaca_trader.is_fractionable("APA")
    print("APA:", apa_fractionable)

    if not apa_fractionable:
        print("APA is not fractionable")
    aapl_fractionable = await alpaca_trader.is_fractionable("AAPL")
    print("AAPL:", aapl_fractionable)
    if not aapl_fractionable:
        print("AAPL is fractionable ")

    return
