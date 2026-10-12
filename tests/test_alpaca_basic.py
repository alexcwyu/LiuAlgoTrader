import time
from datetime import date

import pandas as pd
import pytest

from liualgotrader.common.types import TimeScale
from liualgotrader.data.alpaca import AlpacaData


@pytest.mark.devtest
def test_alpaca_aapl_data_day() -> None:
    alpaca = AlpacaData()
    print(
        alpaca.get_symbol_data(
            "AAPL",
            date(year=2021, month=2, day=1),
            date(year=2021, month=2, day=2),
            scale=TimeScale.day,
        )
    )
    return


@pytest.mark.devtest
def test_alpaca_aapl_data_min() -> None:
    alpaca = AlpacaData()
    print(
        alpaca.get_symbol_data(
            "AAPL",
            date(year=2021, month=2, day=1),
            date(year=2021, month=2, day=2),
        ).between_time("9:30", "16:00")
    )
    return


@pytest.mark.devtest
def test_alpaca_get_symbols() -> None:
    alpaca = AlpacaData()

    t0 = time.time()
    symbols = alpaca.get_symbols()
    t1 = time.time()
    print(
        f"{len(symbols)} symbols are retrieved from Alpaca in {t1-t0} seconds"
    )
    return


@pytest.mark.asyncio
async def test_alpaca_get_market_snapshot() -> None:
    alpaca = AlpacaData()

    t0 = time.time()
    market_snapshots = await alpaca.get_market_snapshot()
    t1 = time.time()
    print(
        f"{len(market_snapshots)} tickers of market snapshots are retrieved from Alpaca in {t1-t0} seconds"
    )
    return


@pytest.mark.devtest
def test_alpaca_multi_symbols_min() -> None:
    alpaca = AlpacaData()
    print(
        alpaca.get_symbols_data(
            ["AAPL", "IBM"],
            date(year=2021, month=2, day=1),
            date(year=2021, month=2, day=2),
        )
    )
    return


@pytest.mark.devtest
def test_alpaca_multi_symbols_day() -> None:
    alpaca = AlpacaData()
    print(
        alpaca.get_symbols_data(
            ["AAPL", "IBM"],
            date(year=2021, month=2, day=1),
            date(year=2021, month=2, day=2),
            TimeScale.day,
        )
    )
    return


@pytest.mark.devtest
def test_alpaca_multi_symbols_min_negative() -> None:
    try:
        AlpacaData().get_symbols_data(
            "AAPL",  # type:ignore
            date(year=2021, month=2, day=1),
            date(year=2021, month=2, day=2),
        )
    except AssertionError:
        return

    raise AssertionError("excepted an error")
