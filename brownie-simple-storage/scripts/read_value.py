from brownie import SimpleStorage, accounts, config

# Contexte :
# Ce script sera lancé sur Rinkeby de manière à exploité le dernier contrat SimpleStorage deployé là-bas
# On le lancera donc de cette manière :
# brownie run scripts/read_value.py --network rinkeby

def read_contract():
    # L'import de SimpleStorage fonctionne comme un Array contenant la liste des adresses auxquelles ont ete
    # déployé ce contrat. SimpleStorage[0] correspond donc à l'adresse du 1er déploiement
    # SimpleStorage[1] est l'adresse du 2ème déploiement
    # L'adresse du déploiement le plus récent est récupéré en parcourant l'Array à l'envers via
    # SimpleStorage[-1] et on récupère de cette manière une instance exploitable de notre contrat
    simple_storage = SimpleStorage[-1]

    # Brownie connait deja l'ABI de notre contrat puisque c'est lui qui l'a compile en utilisant web3.py
    # et qu'il stocke les information dans le dossier `build`
    # On a donc juste à appeler la fonction retrieve pour récuperer la valeur qui est stockée dans le
    # contrat précédemment déployé et exploité dans le scripts `deploy.py`
    print(simple_storage.retrieve())


def main():
    read_contract()
