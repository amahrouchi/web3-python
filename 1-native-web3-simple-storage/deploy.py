import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

# Chargement des var dans le .env
load_dotenv()

# Ce bloc `with` sert à ouvrir le fichier SimpleStorage.sol et à le fermer automatiquement quand le travail est terminé
# La fermeture se fait automatiquement à la fin du bloc `with`
with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Le tuto vidéo ne comprenait pas cette ligne je l'ai trouvée ici :
# https://ethereum.stackexchange.com/questions/110405/having-a-problem-with-solc-x-version-solc-0-6-0-has-not-been-installed
install_solc("0.6.0")

# Compilation
# TODO: regarder plus en détail la dec de solcx pour comprendre toute les possibilités
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the bytecode and the ABI
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connexion à la blockchain locale Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_HTTP_PROVIDER")))
chain_id = int(os.getenv("CHAIN_ID")) # J'ai changé la config Ganache à cause d'une erreur CLI (1337 à la place de 5777)
my_address = os.getenv("PUBLIC_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")  # Ici on a ajouté le préfixe hexa 0x qui n'était pas fourni par Ganache

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address) # on génère le nonce de la transaction en comptant le nombre de transaction effectué par cette adresse sur notre blockchain

# Creation de la transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price, # J'ai ajouté ça parce que sinon ça fonctionnait pas (https://stackoverflow.com/questions/70731492/the-transaction-declared-chain-id-5777-but-the-connected-node-is-on-1337)
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    }
)

# Signature et envoi
print("Deploying contract...")
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Exploité le contrat => on a besoin de son adresse et de son ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Il y a  2 manières d'intéragir avec la blockchain
# Call -> simule un call et recupere la valeur de retour (read sans changement d'état dans la blockchain)
# Transact -> Effectue un changement d'état dans la blockchain

# Valeur initiale du favNumber
print("Initialized fav number:", simple_storage.functions.retrieve().call())
print("Trying to store new fav number with a CALL:", simple_storage.functions.store(88).call())  # Ici on fait un call donc ça exécute la focntion mais ça ne change pas l'état de la blockchain
print("Fav number has not changed =>", simple_storage.functions.retrieve().call())  # comme l'état n'a pas été changé, le favNumber stocké dans le contrat est toujours à 0

# Mise à jour du favNumber de la bonne manière, avec une transaction
print("Updating the fav number...")
store_transaction = simple_storage.functions.store(89).buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1 # on incrémente le nonce ici car il doit être différent de celui de la transaction précédente qui à déployé le contrat
})
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_tx_hash2 = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash2)

print("Fav number updated to:", simple_storage.functions.retrieve().call())
