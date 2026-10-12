import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.data_loader import DataLoader  # type: ignore
from liualgotrader.common.database import create_db_connection
from liualgotrader.consumer import create_strategies_from_db
from liualgotrader.models.tradeplan import TradePlan
from liualgotrader.trading.trader_factory import trader_factory


@pytest_asyncio.fixture(autouse=True)
async def _initialized_resources():
    config.build_label = "pytest"
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
async def test_load_trade_plan_from_db():
    trade_plan = await TradePlan.load()

    for plan in trade_plan:
        print(plan)

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_load_testplan_from_db():

    try:
        strategy_list = await create_strategies_from_db(
            batch_id=str(uuid.uuid4()),
            trader=trader_factory(),
            data_loader=DataLoader(),
        )
    except FileNotFoundError as e:
        print(f"FileNotFoundError {e}")
        return

    print(strategy_list)

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_get_new_entries():
    trade_plan = await TradePlan.get_new_entries(
        since=datetime.now(UTC) - timedelta(days=5)
    )

    for plan in trade_plan:
        print(plan)

    return
