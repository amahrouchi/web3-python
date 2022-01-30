from brownie import accounts, network
from scripts.deploy import deploy
from scripts.utils import get_account, TOKEN_SUPPLY, TOKEN_NAME, TOKEN_SYMBOL, LOCAL_BLOCKCHAIN_ENV
import pytest


def test_token_deployment_successful():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Given
    account = get_account()

    # When
    our_token = deploy()

    # Then
    assert our_token.name() == TOKEN_NAME
    assert our_token.symbol() == TOKEN_SYMBOL
    assert our_token.totalSupply() == TOKEN_SUPPLY
    assert our_token.balanceOf(account) == TOKEN_SUPPLY


def test_transfer_successful():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Given
    account = get_account()
    account2 = get_account(1)
    amountToTransfer = 10

    # When
    our_token = deploy()
    our_token.transfer(account2, amountToTransfer)

    # Then
    assert our_token.balanceOf(account) == TOKEN_SUPPLY - amountToTransfer
    assert our_token.balanceOf(account2) == amountToTransfer

def test_transfer_fails_insufficient_balance():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Given
    account = get_account()
    account2 = get_account(1)
    amountToTranfer = 10

    # When
    our_token = deploy()
    with pytest.raises(AttributeError):
        our_token.transfer(account, amountToTranfer, {"from": account2})
