from brownie import accounts, network, config, OurToken
from scripts.utils import TOKEN_SUPPLY, get_account

def deploy():
    account = get_account()
    our_token = OurToken.deploy(
        TOKEN_SUPPLY,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print("Token deployed!")
    return our_token


def main():
    deploy()
