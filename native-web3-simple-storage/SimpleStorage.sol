// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // Visibilité
    // - public : visible par tout le monde
    // - external : ne peut etre appelé que par un contrat externe
    // - internal : visible par le contrat courant et tous les contrats dérivés de celui-ci (protected)
    // - private : visible uniquement par le contrat courant et aucun autre
    // La visibilité par défaut est "internal"

    // Type de fonction
    // view (lecture):
    // - type de fonction pour uniquement lire dans la blockchain, ce qui ne nécessite pas de faire une transaction (donc pas de frais)
    // - les var public sont automatiquement de fonction 'view'
    // pure (calcul pure):
    // - fonctions qui exécutent des mathématiques pures et ne modifient pas l'état de la blockchain
    // - elle ne font donc pas de transaction non plus

    // Struct
    // Sert à définir des nouveaus types en Solidity

    // Init to 0 when leaved this way
    uint256 favNumber;

    struct People {
        uint256 favNumber;
        string name;
    }
    People public person = People({favNumber: 2, name: "Angelo"});

    /*
     * Creation d'Array de taille dynamique
     */
    People[] public people;

    /*
     * Creation d'Array de taille statique (2 élements max dans cet exemple)
     */
    People[2] public people2;

    /*
     * Mapping(clef => valeur)
     * Lors de la déclaration d'un mapping, on spécifie le type de la clef et le type de la valeur
     */
    mapping(string => uint256) public nameToFavNumber;

    function store(uint256 _favNumber) public returns(uint256){
        favNumber = _favNumber;
        return _favNumber;
    }

    function retrieve() public view returns(uint256) {
        return favNumber;
    }

    function math(uint256 number) public pure {
        number + number;
    }

    // memory : utilisable uniquement pendant l'execution de la fonction (passage par valeur)
    // storage : utilisable au delà de l'execution de la fonction (passage par référence)
    // le type string étant un objet en Solidity, il faut préciser comment on souhaite le passer à la fonction
    function addPerson(string memory _name, uint256 _favNumber) public {

        // Ajout à l'Array
        people.push(People({favNumber: _favNumber, name: _name}));
        // OU
        // people.push(People(_favNumber,_name));
        // Pas besoin de préciser le nom des attributs si on les met dans l'ordre de leur déclaration

        // Ajout au mapping
        nameToFavNumber[_name] = _favNumber;
    }
}
