from io import StringIO
from urllib.parse import urljoin, urlparse
from datetime import date, datetime
from typing import Dict, List

import numpy as np
import pandas as pd
import requests
from lxml import html
import pandas_market_calendars
import pytz
from pandas import DataFrame as df

from liualgotrader.common import config
from liualgotrader.common.data_loader import DataLoader  # type: ignore
from liualgotrader.common.data_loader import m_and_a_data  # type: ignore
from liualgotrader.common.tlog import tlog
from liualgotrader.common.types import TimeScale
from liualgotrader.fincalcs.vwap import add_daily_vwap

volume_today: Dict[str, int] = {}
quotes: Dict[str, df] = {}

NY = "America/New_York"
nytz = pytz.timezone(NY)


def get_symbol_data(
    symbol: str,
    start_date: date,
    end_date: date,
    data_loader=None,
    scale="minute",
) -> df:
    if not data_loader:
        data_loader = DataLoader(TimeScale[scale])

    return data_loader[symbol][start_date:end_date]  # type: ignore


async def get_sector_tickers(sector: str) -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        async with conn.transaction():
            records = await conn.fetch(
                """
                    SELECT symbol
                    FROM ticker_data
                    WHERE sector = $1
                """,
                sector,
            )

            return [record[0] for record in records if record[0]]


async def get_sectors_tickers(sectors: List[str]) -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        async with conn.transaction():
            q = f"""
                    SELECT symbol
                    FROM ticker_data
                    WHERE sector in ({str(sectors)[1:-1]})
                """

            records = await conn.fetch(q)

    return [record[0] for record in records if record[0]]


async def get_industry_tickers(industry: str) -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        records = await conn.fetch(
            """
                SELECT symbol
                FROM ticker_data
                WHERE industry = $1
            """,
            industry,
        )

    return [record[0] for record in records if record[0]]


async def get_industries_tickers(industries: List[str]) -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        q = f"""
                SELECT symbol
                FROM ticker_data
                WHERE industry in ({str(industries)[1:-1]})
            """

        records = await conn.fetch(q)

    return [record[0] for record in records if record[0]]


async def get_market_sectors() -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        records = await conn.fetch("""
                SELECT DISTINCT sector
                FROM ticker_data
            """)
        return [record[0] for record in records if record[0]]


async def get_market_industries() -> List[str]:
    async with config.db_conn_pool.acquire() as conn:
        records = await conn.fetch("""
                SELECT DISTINCT industry
                FROM ticker_data
            """)

        return [record[0] for record in records if record[0]]


_WIKIPEDIA_CONSTITUENTS = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
_WIKIPEDIA_USER_AGENT = (
    "LiuAlgoTrader/0.4.35 "
    "(https://github.com/amor71/LiuAlgoTrader; public market-data research)"
)


def _wikipedia_html(url: str) -> str:
    response = requests.get(
        url, headers={"User-Agent": _WIKIPEDIA_USER_AGENT}, timeout=(5, 20)
    )
    response.raise_for_status()
    return response.text


def _history_table(tables):
    for table in tables:
        if isinstance(table.columns, pd.MultiIndex) and {
            ("Added", "Ticker"),
            ("Removed", "Ticker"),
        }.issubset(table.columns):
            return table
    return None


async def sp500_historical_constituents(date: str):
    """Rewind Wikipedia's published changes and the original ticker rename map.

    The publisher supplies selected history, not an independently certified full
    membership ledger. The current article explicitly links the moved history.
    """
    as_of = pd.Timestamp(date).tz_localize(None)
    tlog(f"loading sp500 constituents for {as_of}")
    article = _wikipedia_html(_WIKIPEDIA_CONSTITUENTS)
    tables = pd.read_html(StringIO(article))
    current = next(table for table in tables if "Symbol" in table.columns)
    symbols = set(current.Symbol.to_list())
    changes = _history_table(tables)
    if changes is None:
        links = html.fromstring(article).xpath(
            '//a[@href and normalize-space(.)="Historical components of the S&P 500"]/@href'
        )
        if not links:
            raise ValueError(
                "Wikipedia article no longer identifies its change history"
            )
        history_url = urljoin(_WIKIPEDIA_CONSTITUENTS, links[0])
        if (
            urlparse(history_url).scheme != "https"
            or urlparse(history_url).netloc != "en.wikipedia.org"
        ):
            raise ValueError("Wikipedia history link leaves the original publisher")
        changes = _history_table(pd.read_html(StringIO(_wikipedia_html(history_url))))
        if changes is None:
            raise ValueError(
                "Linked Wikipedia article has no Added/Removed ticker history"
            )
    date_column = next(
        column for column in changes.columns if column[0] in ("Date", "Effective Date")
    )
    changes = changes.copy()
    changes["date"] = pd.to_datetime(changes[date_column], format="%B %d, %Y")
    tlog(
        f"Wikipedia published history spans {changes['date'].min()} to "
        f"{changes['date'].max()}; reconstructing from its selected changes"
    )
    # Every event is rewound once, latest first. Repeating the entire table can
    # oscillate forever when a company was both added and removed after as_of.
    later = changes.loc[changes["date"] > as_of].sort_values(
        "date", ascending=False, kind="stable"
    )
    for _, row in later.iterrows():
        added, removed = row[("Added", "Ticker")], row[("Removed", "Ticker")]
        if pd.notna(added):
            symbols.discard(added)
        if pd.notna(removed):
            symbols.add(removed)

    actions = m_and_a_data.copy()
    actions.index = pd.to_datetime(actions.index)
    for _, row in (
        actions.loc[actions.index > as_of].sort_index(ascending=False).iterrows()
    ):
        if row.to_symbol in symbols:
            symbols.remove(row.to_symbol)
            symbols.add(row.from_symbol)
    return list(symbols)


async def get_trading_holidays() -> List[str]:
    nyse = pandas_market_calendars.get_calendar("NYSE")
    return nyse.holidays().holidays


async def get_trading_day(now: date, offset: int) -> date:
    cbd_offset = pd.tseries.offsets.CustomBusinessDay(
        n=-offset, holidays=await get_trading_holidays()
    )

    return (now + cbd_offset).date()
