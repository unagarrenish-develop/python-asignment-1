"""Q4: Validate and split transaction CSV records.
Run: python Q4_CSV_Transaction_Splitter.py transactions.csv
Creates credit.csv, debit.csv and error.csv in the current directory.
"""
import csv
import sys
from datetime import datetime

REQUIRED = {"transaction_id", "account_id", "type", "amount", "timestamp"}

def validate_row(row):
    missing = REQUIRED - row.keys()
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    if not row["transaction_id"].strip() or not row["account_id"].strip():
        raise ValueError("Transaction ID and account ID are required")
    kind = row["type"].strip().upper()
    if kind not in ("CREDIT", "DEBIT"):
        raise ValueError("Type must be CREDIT or DEBIT")
    try:
        amount = float(row["amount"])
    except (TypeError, ValueError):
        raise ValueError("Amount is not numeric")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    try:
        datetime.fromisoformat(row["timestamp"].strip())
    except (TypeError, ValueError):
        raise ValueError("Timestamp must be ISO-like")
    return kind, amount

def main():
    if len(sys.argv) != 2:
        print("Usage: python Q4_CSV_Transaction_Splitter.py input.csv", file=sys.stderr)
        return
    balances = {}
    try:
        with open(sys.argv[1], newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            if not reader.fieldnames:
                raise ValueError("Input CSV has no header")
            fields = reader.fieldnames
            with open("credit.csv", "w", newline="", encoding="utf-8") as cf, \
                 open("debit.csv", "w", newline="", encoding="utf-8") as df, \
                 open("error.csv", "w", newline="", encoding="utf-8") as ef:
                credit_writer, debit_writer = csv.DictWriter(cf, fieldnames=fields), csv.DictWriter(df, fieldnames=fields)
                error_fields = fields + ["reason"]
                error_writer = csv.DictWriter(ef, fieldnames=error_fields)
                credit_writer.writeheader(); debit_writer.writeheader(); error_writer.writeheader()
                for row in reader:
                    try:
                        kind, amount = validate_row(row)
                        row["type"] = kind
                        if kind == "CREDIT":
                            credit_writer.writerow(row)
                            balances[row["account_id"]] = balances.get(row["account_id"], 0) + amount
                        else:
                            debit_writer.writerow(row)
                            balances[row["account_id"]] = balances.get(row["account_id"], 0) - amount
                    except (ValueError, TypeError) as exc:
                        error_writer.writerow({**row, "reason": str(exc)})
        for account, balance in sorted(balances.items(), key=lambda item: (-abs(item[1]), item[0])):
            print(account, f"{balance:g}")
    except (OSError, csv.Error, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
