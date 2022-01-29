# Python/Web3 tutorial

## Source

**Video:** 
- https://www.youtube.com/watch?v=M576WGiDBdQ (3h26m30s approximately)

**Source:** 
- https://github.com/smartcontractkit/full-blockchain-solidity-course-py

## Requirements

```
pip install py-solc-x
```

```
pip install web3
```

```
pip install dotenv
```

## Ganache CLI

```
npm install --global ganache
```

## Infura

Application giving us a blockchain URL to connect on a live network

### How to connect to a live blockchain

- Create a project
- In the project settings, change the network you want to connect to
- `.env` file:
    - Change the HTTP URL in the `.env` file to connect to this network
    - Find the `chainId` of your network on the Internet (google it, you'll find it easily)
    - Change your public address and your private key

I personally used the **Rinkeby** test network and used **Metamask** to get my address and my private key.

## Brownie

_(4h27m40s in the video)_

Looks like a Python Ethereum framework.

- Install with `pipx` by following the process described here: https://github.com/eth-brownie/brownie.
- Initialize a Brownie project in the folder of your choice by running:
    - `brownie init`

### Folders

- `build`:
    - contains our compile contracts
    - keeps tracks of all our past deployments on all the different chains we are working with
    - stores the interfaces that we will need
- `contracts`:
    - all the smart contracts developed for our project.
    - when we ask Brownie to compile our contracts, it will automatically look in this folder and compile all our
      contracts.
- `interfaces`:
    - our interfaces
- `reports`:
    - our reports to run
- `scripts`:
    - scripts written automating tasks like deploying, calling different functions...
- `tests`:
    - speaks for itself :)

### Brownie console

You can run an interactive Brownie Python console with:
```
brownie console
```

You can here run any python code related to your brownie project. All your compiled contracts
have already been imported as well as all usefull brownie import like `accounts`, `config`, `network`, ...

It can be really useful to quickly test some code outside of a script.

### Add Ganache UI to Brownie available networks

The problem with the automatic Ganache CLI of Brownie is that Brownie will never remember
deployments. To solve this we can add the Ganache UI to the list of available Brownie
networks by using this command:

```
brownie networks add Ethereum ganache-ui host=http://127.0.0.1:7545 chainid=1337
```

Now we can follow our deployments, transactions... in the Ganache UI and also work with 
previously deployed contracts.

### Fork the Ethereum main net from Alchemy

Video tutorial at: `6:00:55`

We will first need to create an Alchemy account and an Alchemy dev app on the Eth mainnet.
In the following command line you will need to change the fork URL by the one corresponding
to your Alchemy project (Project page > `View key` > Copy the HTTP URL)

```
 brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='<ALCHEMY_URL>' accounts=10 mnemonic=brownie port=8545
```

### About tests

Where to run it:
- Brownie Ganache local environment with mocks **(ALWAYS)**
- Testnet as integretion tests **(ALWAYS)**
- Brownie main net fork **(OPTIONAL)**
- Custom main net fork **(OPTIONAL)**

I personally think that a test on a mainnet forked chain has to be done before any deployment 
on a mainnet. Just to be sure that everything will work as expected in a
mainnet environment

### Brownie mixes

Brownie gives us some boilerplate code templates to start specific projects :
https://github.com/brownie-mix. 

We can init a project with a mix from the command line with:
```
brownie bake <repo_name>
```

Dans le repo `chainlink-mix`, there is already useful contract samples for randomness, pricefeed... and all the tests 
to make sure everything works as expected .A config file is already prepared for us some networks and contract 
addresses preconfigured (Avalanche, polygon,...). We can even run `brownie test [--network <whatever>]` to test 
everything.
