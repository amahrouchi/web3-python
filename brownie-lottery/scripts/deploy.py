from brownie import accounts, network, config, Lottery
from scripts.utils import get_account, get_contract


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth-usd-price-feed").address,
        get_contract("vrf-coordinator").address,
        get_contract("link-token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print("Deployed lottery!")


def main():
    deploy_lottery()
