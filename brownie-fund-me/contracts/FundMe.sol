// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

// Cet import se fait depuis NPM
// Il y a des version 0.8 disponible mais le tuto le fait avec la version 0.6 de Solidity
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// Gestion des overflows (<0.8.0)
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

/**
 * Objectif créer des fonctionnalité capable d'accpter des paiements
 */
contract FundMe {
    // On applique les verifications d'overflow pour les uint256
    // Je pense qu'on ne le fait que pour un seul type car les calculs necessaires
    // peuvent couter du Gas si on les applique partout, c'est une manière d'optimiser
    // les couts en Gas
    using SafeMathChainlink for uint256;

    // Mapping servant à connaitre qui a payé combien via la fonction fund
    mapping(address => uint256) public addressToAmountFounded;

    // La liste des funders que l'on retrouve dans les clefs du mapping précédent
    address[] public funders;

    // L'adresse ayant déployé le contrat
    address public owner;

    constructor() public {
        // Dans le constructeur du contrat, on lui attribue un owner
        // pour pouvoir vérifier qui est capable de retirer les fonds du contrat
        // Le constructeur est appelé au moment ou le smart contract est déployé
        owner = msg.sender;
    }

    function fund() public payable {
        // Mettre en place un minimum pour la transaction en cours
        // On pouurait utiliser ça également pour comparer le prix de vente
        // d'un objet à son équivalent en crypto (ici la crypto en question étant ETH)
        // Ou servir de crowd funding crypto avec un minimum
        uint256 minimumUSD = 50 * 10 ** 18;
        require(getConversionRate(msg.value) > minimumUSD, "You need to spend more ETH!");

        // msg est une variable toujours présente où
        // - sender représente l'addresse qui a appelée cette fonction
        // - value représente le nombre d'eth/gwei/wei envoyé

        // Après l'appel de la fonction fund c'est désormais le smart contract qui est propriétaire
        // des fonds envoyés par le sender de la transaction

        addressToAmountFounded[msg.sender] += msg.value;
        funders.push(msg.sender); // on créé la liste des gens qui ont envoyé de la monnaie sur ce contrat

        // Definition d'une valeur minimale pour la transaction
        // Il est possible de définir cette limite en montant d'autres tokens ou monnaies
        // Par ex si on veut definir en USD, il faut récupérer le ration ETH/USD
    }

    function getVersion() public view returns(uint256){
        // 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e est l'adresse du contrat répondant à l'interface AggregatorV3Interface
        // sur le testnet Rinkeby (sur un autre network l'adresse sera différente)
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        // Ici encore on passe l'adresse du contrat sur le network Rinkeby
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);

        // (
        //     uint80 roundId,
        //     int256 answer,
        //     uint256 startedAt,
        //     uint256 updatedAt,
        //     uint80 answeredInRound
        // ) = priceFeed.latestRoundData();

        // Cet appel peut etre simplifié de cette manière
        // Ce faisant le compilateur ne nous affiche plus de warnings
        (,int256 answer,,,) = priceFeed.latestRoundData();


        return uint256(answer * 10000000000);
        // Le retour est arrondi avec 8 décimal, la somme est donc 3268.43628396 USD/ETH
        // On multiplie par 10^10 pour avoir 18 décimal comme pour le wei, ça simplifiera les calcul plus tard (surement...)
        // Le mec du tuto dit qu'il fait tout le temps comme ça, il doit avoir son expérience et ses raisons
        // donc faisons pareil
    }

    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // On divise par 10^18 parce que les prix ici sont en WEI et on les veut en ETH

        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(
            msg.sender == owner,
            "Cannot withdraw the funds! You are not the owner of this Smart Contract!"
        );
        _;
        // Le _ sert de placeholder pour le code de la fonction qui exécutera le "modifier"
        // S'il est à la fin, le code du modifier (un simple require ici) sera executé avant le code de la fonction qui l'appelle
        // On pourrait également le placer au début pour que modifier s'exécute avant le code de la fonction qui l'appelle
    }

    function withdraw() payable onlyOwner public { // Ici on appelle le modifier que l'on a declaré juste au dessus
        // Permet à celui qui en fait la requête de recupérer le contenu en ETH du contrat
        msg.sender.transfer(address(this).balance);

        // On reset le mapping des gens qui ont participé en remettant leur compteur à 0
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFounded[funder] = 0;
        }

        // On reset également le tableau de funders
        funders = new address[](0);
    }
}