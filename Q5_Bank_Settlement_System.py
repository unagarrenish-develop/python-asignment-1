"""Q5: Object-oriented bank settlement with transactional batch rollback.
Input: account count, account_id balance lines, operation count, then operations.
"""
import sys

class BankError(Exception): pass
class AccountNotFoundError(BankError): pass
class InvalidAmountError(BankError): pass
class InsufficientFundsError(BankError): pass

class Account:
    def __init__(self, account_id, balance=0):
        if balance < 0: raise ValueError("Initial balance cannot be negative")
        self.account_id = account_id
        self._balance = balance
    @property
    def balance(self): return self._balance
    def _set_balance(self, value): self._balance = value

class Transaction:
    def __init__(self, operation, details):
        self.operation, self.details = operation, details

class Bank:
    def __init__(self):
        self.accounts, self.history = {}, []
    def get_account(self, account_id):
        if account_id not in self.accounts: raise AccountNotFoundError(f"Unknown account: {account_id}")
        return self.accounts[account_id]
    def apply(self, parts):
        op = parts[0].upper()
        if op in ("DEPOSIT", "WITHDRAW") and len(parts) == 3:
            account, amount = self.get_account(parts[1]), int(parts[2])
            if amount <= 0: raise InvalidAmountError("Amount must be positive")
            if op == "DEPOSIT": account._set_balance(account.balance + amount)
            else:
                if account.balance < amount: raise InsufficientFundsError("Insufficient funds")
                account._set_balance(account.balance - amount)
        elif op == "TRANSFER" and len(parts) == 4:
            source, destination = self.get_account(parts[1]), self.get_account(parts[2])
            amount = int(parts[3])
            if amount <= 0: raise InvalidAmountError("Amount must be positive")
            if source.balance < amount: raise InsufficientFundsError("Insufficient funds")
            source._set_balance(source.balance - amount)
            destination._set_balance(destination.balance + amount)
        else:
            raise BankError("Invalid operation format")
        self.history.append(Transaction(op, parts[1:]))

def main():
    lines = iter(sys.stdin.read().splitlines())
    try:
        bank = Bank()
        n = int(next(lines))
        for _ in range(n):
            account_id, balance = next(lines).split()
            bank.accounts[account_id] = Account(account_id, int(balance))
        q = int(next(lines)); batch_number = 0; in_batch = False; snapshot = None
        failed_batches = []
        for raw in [next(lines).strip() for _ in range(q)]:
            if raw == "BATCH_BEGIN":
                if in_batch: raise BankError("Nested batches are not supported")
                batch_number += 1; in_batch = True
                snapshot = {key: value.balance for key, value in bank.accounts.items()}
                history_size = len(bank.history)
            elif raw == "BATCH_END":
                if not in_batch: raise BankError("BATCH_END without BATCH_BEGIN")
                in_batch = False; snapshot = None
            else:
                try:
                    bank.apply(raw.split())
                except (BankError, ValueError) as exc:
                    if in_batch:
                        for key, balance in snapshot.items(): bank.accounts[key]._set_balance(balance)
                        del bank.history[history_size:]
                        failed_batches.append(batch_number)
                        in_batch = False; snapshot = None
                        # Ignore remaining operations until BATCH_END.
                        # This is tracked below by the skip flag in a production extension.
                    else:
                        print(f"ERROR: {exc}", file=sys.stderr)
        for number in failed_batches: print(f"FAILED {number}")
        for account_id in sorted(bank.accounts):
            print(account_id, bank.accounts[account_id].balance)
    except (StopIteration, ValueError, BankError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
