# Python/Web3 tutorial

## Source

https://www.youtube.com/watch?v=M576WGiDBdQ (3h26m30s approximately)

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
