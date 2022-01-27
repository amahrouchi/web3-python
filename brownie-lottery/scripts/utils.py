from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract
from web3 import Web3

# Constantes
FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-ui"]
DECIMALS = 8
STARTING_PRICE = 200000000000

# Contract mock mapping
contract_to_mock = {
    "eth-usd-price-feed": MockV3Aggregator,
    "vrf-coordinator": VRFCoordinatorMock,
    "link-token": LinkToken
}


# Récupération du compte
def get_account(index=None, id=None):
    if index:
        return account[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """Cette fonction va récupérer l'adresse du contrat depuis la config
    sinon elle déploiera un mock et renverra ce contrat

    :param contract_name: string - The contract name
    :return: brownie.network.contract.ProjectContract - la version la plus récemment
             déployée de ce contrat.
    """
    contract_type = contract_to_mock[contract_name]

    # Si on est sur un réseau de dev, on deploie un mock et on retourne ce mock
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    # Sinon on récupè l'adresse depuis la config et on instancie le contract depuis la blockchain
    else:
        contract_address = config["network"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi
        )

    return contract


# Déploiement des mocks
def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed!")
