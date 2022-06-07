

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bank:
    pass


@dataclass
class Owner:
    ID: int
    last_name: str
    first_name: str
    street_address: str
    city: str
    state: str

    @classmethod
    def from_csv_line(cls, line):
        ID, last_name, first_name, street_address, city, state = line.strip().split(",")
        return cls(int(ID), last_name, first_name, street_address, city, state)


@dataclass
class Account:
    ID: int
    balance: int = 0
    open_date: datetime = datetime.now()

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")

    @classmethod
    def from_csv_line(cls, line):
        ID, balance, open_date = line.strip().split(",")
        return cls(int(ID), int(balance), datetime.strptime(open_date, "%Y-%m-%d %H:%M:%S %z"))

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.balance < amount:
            print("Insufficient funds")
        else:
            self.balance -= amount

        return self.balance


def main():
    with open("./support/accounts.csv") as f:
        accounts = dict()
        for line in f:
            account = Account.from_csv_line(line)
            accounts[account.ID] = account

    with open("support/owners.csv") as f:
        owners = dict()
        for line in f:
            owner = Owner.from_csv_line(line)
            owners[owner.ID] = owner

    with open("support/account_owners.csv") as f:
        account_owners = [line.strip().split(",") for line in f]
        for account_id, owner_id in account_owners:
            accounts[int(account_id)].owner = owners[int(owner_id)]

    for account in accounts.values():
        print(account)


if __name__ == "__main__":
    main()
