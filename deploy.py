import json
from distutils.version import Version

from solcx import compile_standard, install_solc

# Ce bloc `with` sert à ouvrir le fichier SimpleStorage.sol et à le fermer automatiquement quand le travail est terminé
# La fermeture se fait automatiquement à la fin du bloc `with`
with open("./SimpleStorage.sol", "r") as file:
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
