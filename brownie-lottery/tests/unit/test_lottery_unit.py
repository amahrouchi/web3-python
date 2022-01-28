from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_ENV, STARTING_PRICE, get_account, fund_with_link
import pytest


# Quick and test of our getEntranceFee contract method
# with hard coded values for the account and ETH prices
# def test_get_entrance_fee():
#     account = accounts[0]
#     lottery = Lottery.deploy(
#         config["networks"][network.show_active()]["eth-usd-price-feed"],  # 1er param du constructeur du contrat Lottery
#         {"from": account}
#     )
#
#     # Quick and dirty assertion
#     # At the date I write this script 1 ETH <=> $2535.27
#     # So $50 <=> 0.019772 ETH
#     assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
#     assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Arrange
    lottery = deploy_lottery()

    # Act
    entrance_fee = lottery.getEntranceFee()
    # 50 est le prix d'entrée dans la lottery (en dur dans le contrat)
    # 2000 est le prix passé dans le constructeur de MockV3Aggregator (voir le fichier utils.py => STARTING_PRICE)
    # Le prix d'entrée est donc (50 / 2000) ether qu'il faut transformer en WEI pour être exploitable
    expected_fee = Web3.toWei(
        50 / (STARTING_PRICE / (10 ** 8)),  # 50 / 2000
        "ether"
    )

    # Assert
    assert expected_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Act / Assert
    lottery = deploy_lottery()
    # with pytest.raises(exceptions.VirtualMachineError): # dans le tuto c'était cette ligne
    with pytest.raises(AttributeError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Act
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # Assert
    assert lottery.players(0) == account
    # Un array recupérer depuis un contrat doit être utilisé comme une fonction
    # donc avec des () et pas de []


def test_can_end_lottery():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    # Act
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    # Assert
    assert lottery.lotteryState() == 2
