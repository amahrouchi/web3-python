from brownie import FundMe, accounts, network
from scripts.utils import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    eth_price = fund_me.getPrice()
    print(f"ETH price is: {eth_price} Wei")
    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance fee: {entrance_fee} Wei")
    print("Funding...")
    fund_me.fund({
        "from": account,
        "value": entrance_fee # Le nombre d'ETH que  l'on souhaite envoyer
    })

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from":  account})

def main():
    fund()
    withdraw()
