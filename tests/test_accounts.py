import asyncio

import pytest
import pytest_asyncio

from liualgotrader.common import config
from liualgotrader.common.database import create_db_connection
from liualgotrader.models.accounts import Accounts


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
async def test_create() -> None:
    account_id = await Accounts.create(
        balance=1000.0,
        allow_negative=True,
        credit_line=2000.0,
    )
    print(f"new account_id:{account_id}")

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_negative_create() -> None:
    try:
        await Accounts.create(
            balance=1000.0,
            allow_negative=True,
        )
    except Exception as e:
        print(e)

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_balance() -> None:
    balance = 1234.0
    account_id = await Accounts.create(
        balance=balance,
        allow_negative=True,
        credit_line=2000.0,
    )
    print(f"new account_id:{account_id}")
    if balance != await Accounts.get_balance(account_id):
        raise AssertionError("get_balance() did not return the expect value")
    print(f"balance {balance}")
    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_add_transaction() -> None:
    balance = 1234.0
    account_id = await Accounts.create(
        balance=balance,
        allow_negative=True,
        credit_line=2000.0,
    )
    amount = 1000.0
    await Accounts.add_transaction(account_id, amount)
    if balance + amount != await Accounts.get_balance(account_id):
        raise AssertionError(
            "test_add_transaction(): get_balance() did not return the expect value"
        )

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_add_transaction2() -> None:
    balance = 1234.0
    account_id = await Accounts.create(
        balance=balance,
        allow_negative=True,
        credit_line=2000.0,
    )
    amount = 1000.0
    await Accounts.add_transaction(account_id, amount)
    await Accounts.add_transaction(account_id, -amount)
    if balance != await Accounts.get_balance(account_id):
        raise AssertionError(
            "test_add_transaction(): get_balance() did not return the expect value"
        )

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_add_transaction3() -> None:
    balance = 1234.0
    account_id = await Accounts.create(
        balance=balance,
        allow_negative=False,
    )
    amount = 1000.0
    await Accounts.add_transaction(account_id, amount)
    await Accounts.add_transaction(account_id, -amount)
    if balance != await Accounts.get_balance(account_id):
        raise AssertionError(
            "test_add_transaction3(): get_balance() did not return the expect value"
        )

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_add_transaction5() -> None:
    balance = 100.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=5000.0
    )
    amount = 1000.0
    await Accounts.add_transaction(account_id, -amount)
    if balance - amount != await Accounts.get_balance(account_id):
        raise AssertionError(
            "test_add_transaction5(): get_balance() did not return the expect value"
        )

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_clear_balance() -> None:
    print("test_clear_balance")
    balance = 1234.0
    account_id = await Accounts.create(
        balance=balance,
        allow_negative=True,
        credit_line=2000.0,
    )
    print(f"new account_id:{account_id}")
    if balance != await Accounts.get_balance(account_id):
        raise AssertionError("get_balance() did not return the expect value")

    print(f"balance {balance}")

    await Accounts.clear_balance(account_id, 0)
    if await Accounts.get_balance(account_id) != 0.0:
        raise AssertionError("clear balance failed")

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_clear_transactions() -> None:
    print("test_clear_transactions")
    balance = 100.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=5000.0
    )
    amount = 1000.0
    await Accounts.add_transaction(account_id, -amount)
    if balance - amount != await Accounts.get_balance(account_id):
        raise AssertionError(
            "test_clear_transactions(): get_balance() did not return the expect value"
        )

    await Accounts.clear_account_transactions(account_id)
    _df = await Accounts.get_transactions(account_id)
    if not _df.empty:
        raise AssertionError(
            "test_clear_transactions(): failed to clear account_transactions"
        )

    return


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_check_if_enough_balance_positive_1() -> None:
    print("test_check_if_enough_balance_positive_1")

    balance = 1000.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=False, credit_line=0.0
    )

    if await Accounts.check_if_enough_balance_to_withdraw(account_id, 500.0):
        return
    else:
        raise AssertionError(
            "test_check_if_enough_balance_positive_1(): should have had enough balance"
        )


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_check_if_enough_balance_positive_2() -> None:
    print("test_check_if_enough_balance_positive_2")

    balance = 1000.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=500.0
    )

    if not await Accounts.check_if_enough_balance_to_withdraw(
        account_id, 2000.0
    ):
        return
    else:
        raise AssertionError(
            "test_check_if_enough_balance_positive_2(): should not have had enough balance"
        )


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_check_if_enough_balance_positive_3() -> None:
    print("test_check_if_enough_balance_positive_3")

    balance = 1000.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=500.0
    )
    await Accounts.add_transaction(account_id, -1100)

    if await Accounts.check_if_enough_balance_to_withdraw(account_id, 200.0):
        return
    else:
        raise AssertionError(
            "test_check_if_enough_balance_positive_3(): should  have had enough balance"
        )


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_check_if_enough_balance_positive_4() -> None:
    print("test_check_if_enough_balance_positive_4")

    balance = 1000.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=500.0
    )
    await Accounts.add_transaction(account_id, -1100)

    if not await Accounts.check_if_enough_balance_to_withdraw(
        account_id, 600.0
    ):
        return
    else:
        raise AssertionError(
            "test_check_if_enough_balance_positive_4(): should not have had enough balance"
        )


@pytest.mark.asyncio
@pytest.mark.devtest
async def test_check_if_enough_balance_negative_1() -> None:
    print("test_check_if_enough_balance_negative_1")

    balance = 1000.0
    account_id = await Accounts.create(
        balance=balance, allow_negative=True, credit_line=500.0
    )
    try:
        not await Accounts.check_if_enough_balance_to_withdraw(
            account_id, -600.0
        )
    except AssertionError:
        return

    raise AssertionError(
        "test_check_if_enough_balance_negative_1(): should have raise exception"
    )
