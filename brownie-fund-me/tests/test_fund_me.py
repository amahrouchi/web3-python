from scripts.utils import get_account
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    # arrange
    account = get_account()
    fund_me = deploy_fund_me()

    # act/assert
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # act/assert
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0
