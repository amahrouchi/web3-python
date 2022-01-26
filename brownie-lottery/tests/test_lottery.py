from brownie import Lottery, accounts, config, network
from web3 import Web3

# Quick and test of ou r getEntranceFee contract method
# with hard coded values for the account and ETH prices
def test_get_entrance_fee_dirty():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth-usd-price-feed"],  # 1er param du constructeur du contrat Lottery
        {"from": account}
    )

    # Quick and dirty assertion
    # At the date I write this script 1 ETH <=> $2535.27
    # So $50 <=> 0.019772 ETH
    assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")
