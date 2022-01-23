from brownie import network, config, FundMe, MockV3Aggregator
from scripts.utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENV


def deploy_fund_me():
    account = get_account()

    # Ici on rajoutera l'option publish_source si on source publier les sources de notre contrat sur Etherscan
    # (ce qui peut ne pas être notre souhait si on ne veut pas rendre notre contrat utilisable publiquement je pense)
    # Pour se faire il fait se créer un compte sur Etherscan.io, puis aller y créer un clef d'API que l'on ajouter
    # dans notre fichier .env en la nommant ETHERSCAN_TOKEN
    # Grâce à cela nous seront capable dans Etherscan de visualiser le code source de notre contrat dans l'onglet
    # "Contracts" d'Etherscan (sans cela c'est un binaire illisible qui apparaît là) et aussi d'appeler les fonctions
    # publiques du contrat

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()]["eth-usd-price-feed-address"]
        # Il faudra en plus vérifier ici que la clef config["networks"][network.show_active()] existe bien dans la
        # config et raise un exception dans le cas contraire
    else:
        # On déploie ici le mock du priceFeed (si necessaire) et on en récupère l'adresse
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,  # 1er paramètre du constructeur de notre contrat en Solidity
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
        # La fonction .get() sert à gérer automatiquement le cas où la clef verify serait absente
        # Et ça doit mettre False par défaut je suppose
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
