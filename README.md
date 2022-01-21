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
