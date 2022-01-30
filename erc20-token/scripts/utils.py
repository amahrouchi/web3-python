from brownie import accounts, network, config

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-ui"]
TOKEN_NAME = "Our Token"
TOKEN_SYMBOL = "OTK"
TOKEN_DECIMALS = 18
TOKEN_SUPPLY = 1000 * (10 ** TOKEN_DECIMALS)


# Récupération du compte
def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
