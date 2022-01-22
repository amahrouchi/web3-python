from brownie import SimpleStorage, accounts


# Les tests sont lancés avec la commande `brownie test` cette commande jouera tous les tests disponibles
# `brownie test -k <function-name>` jouera uniquement la fonction nommée en param
# `brownie test --pdb` à la fin du test on entre dans une invite de commande Python dans l'état dans lequel le script
# s'est arrêté ce qui permet de vérifier l'état des variables et de lancer des appels de contrat par exemple
# pour vérifier ce qui ne fonctionnerait pas
# `brownie test --s` verbose mode pour plus de détails sur les tests exécutés

# Le framework de test utilisé ici est pytest et toutes les fonctionnalité de Pytest sont disponibles à travers
# Brownie donc pour plus de fonctionnalité il faudra RTFM la doc de Pytest !

def test_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    expected = 15
    simple_storage.store(15, {"from": account})

    # Assert
    assert simple_storage.retrieve() == expected
