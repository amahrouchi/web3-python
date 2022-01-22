from brownie import accounts, config, SimpleStorage, network

# Lors de l'execution d'un script si on ne précise pas de network par défaut
# Brownie va se connecter à Ganache CLI

# Brownie est nativement compatible avec un certain nombre de réseau blockchain locaux, test ou live
# `brownie networks list` va nous donner cette liste avec les identidiants à utiliser (en vert)
# Pour lancer un script directement dans le network désiré on lancera donc :
# `brownie run scripts/deploy.py --network rinkeby` pour lancer notre script sur Rinkeby
# Brownie étant nativement compatible avec Infura, il suffit de rajouter une clef `WEB3_INFURA_PROJECT_ID`
# dans notre `.env` pour utiliser le service Infura pour se connecter à Rinkeby

def deploy_simple_storage():
    # Ganache : Brownie peut automatiquement exploiter les comptes disponibles dans Ganache
    # si aucun compte n'est précisé
    # account = accounts[0]

    # Compte personnalisé
    # Ce compte est créé via la commande `brownie accounts new <account_name>`
    # qui va nous demander la clef privée et un mot de passe pour la sécuriser
    # account = accounts.load("metamask")

    # Compte depuis des variables d'environnement
    # Grace aux fichiers .env et brownie-config.yaml qui permettent de mettre en place des env-vars
    # De cette manière, on a pas besoin de taper le mdp du compte précédemment ajouté à chaque fois
    # Remarque : en cas de piratage de notre serveur c'est la merde, puisque nos clefs privées sont lisibles en env...
    # 2 manières
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"]) # voir le fichier brownie-config.yaml pour comprendre

    account = get_account()
    # print(account)

    # Déploiement du contrat
    # Une fois compilé le contrat peut etre directement importé depuis Brownie (voir l'import SimpleStorage en haut)
    # Pour compiler un contrat on lance `brownie compile` et tous les contrats du dossier `contracts` seront compilés
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()  # retrieve is a CALL (read-only view) function so we don't need to specify the `from` address
    print(stored_value)
    transaction = simple_storage.store(88, {"from": account})  # Here we specify the from address because we are making a state change
    transaction.wait(1) # comme dans web3.py on attend ici que le block soit miné pour être sûr que notre transaction est ok (1 est le nombre de block qu'on souhaite attendre)
    updated_value = simple_storage.retrieve()
    print(updated_value)

    # On voit qu'avec Brownie, il est beaucoup plus rapide de compiler, déployer et exploiter un contrat sur blockchain
    # La quantité de code de ce fichier comparé à celle du deploy.py du dossier `native-web3-simple-storage`
    # est incomparable. Brownie nous épargne beaucoup de travail ce qui est plutôt cool !

# Ici si on est en mode local, on se connecte à Ganache
# si on est mode live, on utilise l'account stocké dans nos variables d'env
# Le mode live est déclenché par la option `--network` utilisée lors du lancement du script :
# `brownie run scripts/deploy.py --network rinkeby` par ex.
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()
