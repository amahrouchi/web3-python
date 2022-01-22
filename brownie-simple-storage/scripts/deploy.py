from brownie import accounts, config, SimpleStorage

# Lors de l'execution d'un script si on ne précise pas de network par défaut
# Brownie va se connecter à Ganache CLI

def deploy_simple_storage():
    # Ganache : Brownie peut automatiquement exploiter les comptes disponibles dans Ganache
    # si aucun compte n'est précisé
    account = accounts[0]

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


def main():
    deploy_simple_storage()
