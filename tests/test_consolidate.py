import pytest
from hypothesis import example, given, settings
from hypothesis.strategies import text

from liualgotrader.analytics.consolidate import trades
from liualgotrader.common import config


@settings(deadline=None, max_examples=3)  # type: ignore
@given(text())
@pytest.mark.asyncio
@pytest.mark.devtest
async def test_trades(batch_id: str) -> None:
    previous_pool = getattr(config, "db_conn_pool", None)
    try:
        await trades(batch_id)
    finally:
        pool = getattr(config, "db_conn_pool", None)
        if pool is not None and pool is not previous_pool:
            await pool.close()
            if getattr(config, "db_conn_pool", None) is pool:
                del config.db_conn_pool
