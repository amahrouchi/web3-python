from distutils.version import Version

from solcx import compile_standard, install_solc

# Ce bloc `with` sert à ouvrir le fichier SimpleStorage.sol et à le fermer automatiquement quand le travail est terminé
# La fermeture se fait automatiquement à la fin du bloc `with`
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compilation
# TODO: regarder plus en détail la dec de solcx pour comprendre toute les possibilités
install_solc("0.6.0") # Le tuto vidéo
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

print(compiled_sol)
