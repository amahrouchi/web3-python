from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract, interface
# from web3 import Web3

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
        return accounts[index]

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
    # Sinon on récupère l'adresse depuis la config et on instancie le contract depuis la blockchain
    # et on connait sont ABI grace aux mocks que l'on a créé (l'ABI d'un mock et du vrai contrat est la même,
    # c'est le principe d'un mock en fait)
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
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


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):  # 0.1 LINK
    account = account if account else get_account()

    # Manière 1 de recup un contrat.
    # On rappelle que get_contract() utilise Contract.from_abi() pour créer le contrat
    # cette méthode demande de connaitre l'ABI du contract et son adresse
    # ===================================================================
    link_token = link_token if link_token else get_contract("link-token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # ===================================================================

    # Manière 2 de récupérer un contract
    # Via `interface` dans brownie + l'addresse du contrat en question
    # l'interface sera compilé en une ABI de contrat utilisable
    # et le contrat sera créé à partir de cette ABI et de l'adresse du contrat sur la blockchain
    # ===================================================================
    # link_token = interface.LinkTokenInterface(link_token.address)
    # tx = link_token.transfer(contract_address, amount, {"from": account})
    # ===================================================================

    # Quelques commentaires sur ces 2 méthode
    # De ce que je comprends, l'adresse du contrat ne suffit pas probablement parce que c'est juste
    # du binaire stocké sur une adresse dans la blockchain. Par contre, avec l'ABI en plus de l'adresse,
    # on connait la carte qui nous permet d'exploiter ce binaire de manière efficace

    tx.wait(1)
    print("Contract funded with some LINK!")

    return tx
