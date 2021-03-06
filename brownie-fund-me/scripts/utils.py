from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

# Constantes
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-ui"]
DECIMALS = 8
STARTING_PRICE = 200000000000

# Récupération du compte
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


# Déploiement des mocks
def deploy_mocks():
    # Ici à la place de récupérer le contrat de price feed depuis la blockchain
    # on déploie un mock de ce priceFeed que l'on va utiliser de manière transparente
    # De ce fait, notre script est maintenant agnostique de l'environnement dans lequel il tourne
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        # MockV3Aggregator.deploy(
        #     DECIMALS,  # _decimals => 1er param du construct du contrat, nombre de décimales utilisées
        #     Web3.toWei(STARTING_PRICE, "ether"),  # _initialAnswer => 2eme param du construct du contrat (2000 * 10^18)
        #     {"from": get_account()}
        # )
        MockV3Aggregator.deploy(
            DECIMALS,  # _decimals => 1er param du construct du contrat, nombre de décimales utilisées
            STARTING_PRICE,  # _initialAnswer => 2eme param du construct du contrat
            {"from": get_account()}
        )

    print("Mocks deployed!")
