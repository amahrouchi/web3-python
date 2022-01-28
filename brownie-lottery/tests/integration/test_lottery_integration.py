from brownie import network
from scripts.utils import LOCAL_BLOCKCHAIN_ENV, get_account, fund_with_link
from scripts.deploy import deploy_lottery
import pytest
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(300)  # Pour le test, on attend que ChainLink reponde avec le nb aléatoire (300sec = 5min)
    # Il semblerait que la réponse sur Rinkeby mette 3min+ à arriver (le type avait mis 1 min dans le tuto)
    # Dans un cas de prod, il faudrait plutôt faire une lecture continue jusqu'à ce que l'adresse
    # soit différente de 0x00000000...

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
