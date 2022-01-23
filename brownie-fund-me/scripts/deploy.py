from brownie import FundMe
from scripts.utils import get_account


def deploy_fund_me():
    account = get_account()

    # Ici on rajoutera l'option publish_source si on source publier les sources de notre contrat sur Etherscan
    # (ce qui peut ne pas être notre souhait si on ne veut pas rendre notre contrat utilisable publiquement je pense)
    # Pour se faire il fait se créer un compte sur Etherscan.io, puis aller y créer un clef d'API que l'on ajouter
    # dans notre fichier .env en la nommant ETHERSCAN_TOKEN
    # Grâce à cela nous seront capable dans Etherscan de visualiser le code source de notre contrat dans l'onglet
    # "Contracts" d'Etherscan (sans cela c'est un binaire illisible qui apparaît là) et aussi d'appeler les fonctions
    # publiques du contrat
    fund_me = FundMe.deploy({"from": account}, publish_source=True)
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
