import asyncio
import uuid

import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.models.keystore import KeyStore

strategy_name: str = str(uuid.uuid4())
context: str = str(uuid.uuid4())


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
async def test_load_empty() -> None:
    data = await KeyStore.load("some_lie")

    if data:
        raise AssertionError(f"empty field must be None and not {data}")

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_insert() -> None:
    await KeyStore.save("k1", "v1")
    data = await KeyStore.load("k1")

    if data != "v1":
        raise AssertionError("failed to insert and load key")

    print(f"test_insert: {strategy_name} k1={data}")
    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_update() -> None:
    await KeyStore.save("k2", "v21")
    data = await KeyStore.load("k2")

    if data != "v21":
        raise AssertionError("failed to insert and load key")

    await KeyStore.save("k2", "v22")
    data = await KeyStore.load("k2")
    if data != "v22":
        raise AssertionError("failed to update and load key")

    print(f"test_update: {strategy_name} k2={data}")

    return
