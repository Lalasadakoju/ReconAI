import json
import random
from datetime import datetime, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def generate_transaction_id(prefix, number):
    return f"{prefix}{number:04d}"


def generate_synthetic_data(num_records=120):
    """
    Generates synthetic payment gateway and bank settlement records.
    Some records intentionally contain mismatches, delays,
    duplicates, and missing settlements.
    """

    random.seed(42)

    DATA_DIR.mkdir(exist_ok=True)

    gateway_records = []
    bank_records = []
    ground_truth = []

    base_time = datetime(2026, 9, 1, 9, 0, 0)

    for i in range(1, num_records + 1):

        transaction_id = generate_transaction_id("TXN", i)

        amount = random.choice([
            199, 299, 499, 599, 799,
            999, 1200, 1500, 2000,
            2500, 5000
        ])

        transaction_time = base_time + timedelta(
            minutes=random.randint(0, 4320)
        )

        customer_id = f"CUST{random.randint(1, 40):03d}"

        gateway_record = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "amount": amount,
            "timestamp": transaction_time.isoformat(),
            "status": "SUCCESS"
        }

        gateway_records.append(gateway_record)

        scenario = random.choices(
            [
                "exact_match",
                "minor_amount_difference",
                "delayed_settlement",
                "missing_settlement",
                "duplicate_settlement"
            ],
            weights=[55, 15, 15, 10, 5],
            k=1
        )[0]

        if scenario == "missing_settlement":

            ground_truth.append({
                "transaction_id": transaction_id,
                "expected_status": "UNRESOLVED",
                "scenario": scenario
            })

            continue

        settlement_delay = random.randint(1, 60)

        if scenario == "delayed_settlement":
            settlement_delay = random.randint(120, 1440)

        bank_amount = amount

        if scenario == "minor_amount_difference":
            bank_amount = amount + random.choice([-1, 1, -2, 2])

        bank_record = {
            "bank_reference": generate_transaction_id("BNK", i),
            "customer_id": customer_id,
            "amount": bank_amount,
            "timestamp": (
                transaction_time +
                timedelta(minutes=settlement_delay)
            ).isoformat(),
            "status": "SETTLED"
        }

        bank_records.append(bank_record)

        if scenario == "duplicate_settlement":

            duplicate_record = bank_record.copy()

            duplicate_record["bank_reference"] = (
                generate_transaction_id("BNKDUP", i)
            )

            duplicate_record["timestamp"] = (
                transaction_time +
                timedelta(minutes=settlement_delay + 5)
            ).isoformat()

            bank_records.append(duplicate_record)

        expected_status = "MATCHED"

        ground_truth.append({
            "transaction_id": transaction_id,
            "expected_status": expected_status,
            "scenario": scenario
        })

    gateway_path = DATA_DIR / "gateway_transactions.json"
    bank_path = DATA_DIR / "bank_settlements.json"
    truth_path = DATA_DIR / "ground_truth.json"

    with open(gateway_path, "w", encoding="utf-8") as file:
        json.dump(gateway_records, file, indent=4)

    with open(bank_path, "w", encoding="utf-8") as file:
        json.dump(bank_records, file, indent=4)

    with open(truth_path, "w", encoding="utf-8") as file:
        json.dump(ground_truth, file, indent=4)

    return {
        "gateway_records": len(gateway_records),
        "bank_records": len(bank_records),
        "ground_truth_records": len(ground_truth),
        "files_created": [
            str(gateway_path),
            str(bank_path),
            str(truth_path)
        ]
    }


if __name__ == "__main__":

    result = generate_synthetic_data()

    print("\nSynthetic financial data generated successfully!\n")

    print(f"Gateway records: {result['gateway_records']}")
    print(f"Bank records: {result['bank_records']}")
    print(
        f"Ground truth records: "
        f"{result['ground_truth_records']}"
    )