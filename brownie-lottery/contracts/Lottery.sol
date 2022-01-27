// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable, VRFConsumerBase {

    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;

    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LotteryState {
        OPEN, // 0
        CLOSED, // 1
        CALCULATING_WINNER // 2
    }
    LotteryState public lotteryState;

    // On ajoute aussi ça parce qu'on va avoir besoin d'un pour utiliser le contrat RandomNumberConsumer
    // On les ajoute donc ici mais aussi dans le constructeur parce que les valeurs vont varier en fonction
    // de la blockchain sur laquelle le contrat RandomNumberConsumer sera utilisé (mainnet Chainlink, testnet ChainLink...)
    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    )
    public
    VRFConsumerBase (_vrfCoordinator, _link) // Ici on passe les paramètres du constructeur hérité
    {
        usdEntryFee = 50 * (10 ** 18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LotteryState.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // $50 minimum
        require(lotteryState == LotteryState.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH, $50 minimum");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        // Documentation du price feed: https://docs.chain.link/docs/ethereum-addresses

        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();

        // La documentation indique que le prix de la paire ETH/USD arrive avec 8 décimales
        // Si on le veut avec 18 décimales pour l'exprimer en WEI on multiplie par 10^10
        uint256 adjustedPrice = uint256(price) * (10 ** 10);
        // 18 décimales ici

        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    // Le modifier onlyOwner vient du contrat Ownable d'OpenZeppelin
    function startLottery() public onlyOwner {
        require(lotteryState == LotteryState.CLOSED, "Can't start the lottery yet!");
        lotteryState = LotteryState.OPEN;
    }

    function endLottery() public onlyOwner {
        // Les gens pensent à tort que block.difficulty est une variable globale proche
        // et utilisent ce type de code pour générer un nombre aléatoire
        // Cependant block.difficulty est un variable qui peut etre manipulé par les mineurs
        // donc qqun de smart pourrait en profiter et gagner la lotterie
        // uint256(
        //     keccack256(
        //         abi.encodedPacked(
        //             nonce, // nonce => predictable
        //             msg.sender, // msg.sender => predictable
        //             block.difficulty, // block.difficulty can be manipulated by miners
        //             block.timestamp // block.timestamp is predictable
        //         )
        //     )
        // ) % players.length;

        // On verrouille les participations et le démarrage en changeant l'état
        lotteryState = LotteryState.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);

        // Ici dans une 1ere transaction on fait une requete vers chainlink pour recevoir un numéro aléatoire
        // mais il va falloir attendre la réponse de Chainlink dans une autre transaction pour pouvoir l'exploiter
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lotteryState == LotteryState.CALCULATING_WINNER, "You aren't there yet!");
        require(_randomness > 0, "Random number not found!");

        uint256 winnerIndex = _randomness % players.length;
        recentWinner = players[winnerIndex];
        recentWinner.transfer(address(this).balance);

        players = new address payable[](0);
        lotteryState = LotteryState.CLOSED;
        randomness = _randomness;
    }
}
