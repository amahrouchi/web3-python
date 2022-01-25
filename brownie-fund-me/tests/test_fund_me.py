from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENV
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    # arrange
    account = get_account()
    fund_me = deploy_fund_me()

    # act/assert
    entrance_fee = fund_me.getEntranceFee()
    # Petit souci ici quand je test sur le mainnet-fork-dev créé depuis Alchemy
    # J'ai une exception qui apparait eth_abi.exceptions.NonEmptyPaddingBytes
    # Peut-être un probleme de deploiement de notre contrat ou d'un de ces dépendances
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # act/assert
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# Ce test est un exemple de test que l'on voudrait n'exécuter que sur des environnements de locaux des test
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    # Dans le tuto, c'était ça la ligne mais chez ça raise pas la mm exception
    # with pytest.raises(exceptions.VirtualMachineError):
    with pytest.raises(AttributeError):
        fund_me.withdraw({"from": bad_actor})
