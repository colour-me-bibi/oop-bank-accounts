

from argparse import ArgumentError
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


class SavingsAccount(Account):
    def __init__(self, ID, balance, open_date):
        super().__init__(ID, balance, open_date)

        if self.balance < 10:
            raise ArgumentError("Initial balance cannot be less than 10!")

    def add_interest(self, rate=0.25):
        interest = self.balance * rate / 100

        self.balance += interest

        return interest

    def withdraw(self, amount):
        new_balance = self.balance - amount + 2

        if new_balance < 10:
            print("Insufficient funds!")
            return self.balance

        self.balance = new_balance
        return self.balance


class CheckingAccount(Account):
    def __init__(self, ID, balance, open_date):
        super().__init__(ID, balance, open_date)
        self.check_count = 0

    def withdraw(self, amount):
        new_balance = self.balance - amount + 1

        if new_balance < 0:
            print("Insufficient funds!")
            return self.balance

        self.balance = new_balance
        return self.balance

    def withdraw_using_check(self, amount):
        check_fee = 2 if self.check_count > 3 else 0

        new_balance = self.balance - amount + check_fee

        self.check_count += 1

        if new_balance < -10:
            print("Insufficient funds!")
            return self.balance

        self.balance = new_balance
        return self.balance

    def reset_checks(self):
        self.check_count = 0


class MoneyMarketAccount(Account):
    def __init__(self, ID, balance, open_date):
        super().__init__(ID, balance, open_date)
        self.transaction_count = 0

        if self.balance < 10000:
            raise ArgumentError("Initial balance cannot be less than 10000!")

    def add_interest(self, rate=0.25):
        interest = self.balance * rate / 100

        self.balance += interest

        return interest

    def deposit(self, amount):
        if self.balance < 10000 and self.balance + amount > 100000:
            self.balance += amount
            return self.balance

        if self.transaction_count > 6:
            print("You cannot make any more transactions!")
            return self.balance

        self.transaction_count += 1
        self.balance += amount

        return self.balance

    def withdraw(self, amount):
        if self.transaction_count > 6:
            print("You have no more transactions!")
            return self.balance

        if self.balance < 10000:
            print("You must deposit more funds!")
            return self.balance

        self.transaction_count += 1
        self.balance -= amount

        if self.balance < 10000:
            print("This withdrawl dropped your account below $10000 so you get a $100 fee!")
            self.balance -= 100

        return self.balance

    def reset_transactions(self):
        self.transaction_count = 0


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
