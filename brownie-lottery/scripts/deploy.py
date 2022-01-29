from brownie import accounts, network, config, Lottery
from scripts.utils import get_account, get_contract, fund_with_link
import time

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
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # Il vaut mieux toujours après une transaction attendre qu'elle ait été validé par la blockchain
    # sinon on peut rencontrer des erreurs. Dans mon cas, je n'en ai pas eu mais le mec dans le tuto oui
    # avec une histoire d'erreur liée au statut de la transaction probablement
    # https://www.youtube.com/watch?v=M576WGiDBdQ à 7h36m12s
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # Ici on récupère la valeur minimale pour participer à la loterie
    value = lottery.getEntranceFee() + 1000  # On ajoute qq WEI pour être sûr d'être au dessus de la valeur minimale

    # On lance la transaction en précisant le compte participant à la loterie et la valeur de la participation
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    link_tx = fund_with_link(lottery.address)
    link_tx.wait(1)

    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    print(f"The lottery has ended! Waiting for the winner to be determinated...")

    # Ici on attend la réponse du noeud chainlink à notre demande de nombre aléatoire
    # dans mon cas 60 n'a pas suffit, il faudrait plutot faire un boucle infinie (15 min max je pense)
    # et attendre que le winner soit différent de 0
    time.sleep(60)
    print(f"Winner is {lottery.recentWinner()}") # Les attributs publics d'un contrat doivent être appelé avec des ()

    # Sur une blockchain locale type Ganache, il n'y a pas de noeud ChainLink qui répondra à notre appel
    # via la méthode fulfillRandomness de notre contrat de Lottery du coup aucun gagnant ne peut être déterminé


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
