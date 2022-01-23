// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

// Cet import se fait depuis NPM
// Il y a des version 0.8 disponible mais le tuto le fait avec la version 0.6 de Solidity
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// Gestion des overflows (<0.8.0)
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // On applique les verifications d'overflow pour les uint256
    // Je pense qu'on ne le fait que pour un seul type car les calculs necessaires
    // peuvent couter du Gas si on les applique partout, c'est une manière d'optimiser
    // les couts en Gas
    using SafeMathChainlink for uint256;

    // Mapping funders => montant donné
    mapping(address => uint256) public addressToAmountFounded;

    // La liste des funders
    address[] public funders;

    // L'adresse owner du contrat
    address public owner;

    // Contrat permettant la récupération des prix de l'ether (Chainlink)
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;

        // On instancie ici notre priceFeed Chainlink depuis le constructeur
        // Ce sera un parametre passé à la fonction de déploiement de Brownie
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10 ** 18;
        require(getConversionRate(msg.value) > minimumUSD, "You need to spend more ETH!");

        addressToAmountFounded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint256){
        // Comme le priceFeed est instancié dans le constructeur, dans cette version du smart contract, on a pas besoin
        // de spécifier l'adresse du contrat en dur, elle sera donnée en paramètre du déploiement via Brownie dans
        // le script Python

        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        // Idem ici par rapport à la fonction précédente, on a plus besoin de récupérer le contrat avec son
        // adresse en dur

        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
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
    }

    function withdraw() payable onlyOwner public {
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