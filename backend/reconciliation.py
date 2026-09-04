import json
import time
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename):
    """Load a JSON file from the data directory."""

    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_similarity(gateway, bank):
    """
    Calculate a confidence score between a gateway transaction
    and a bank settlement record.

    The score is based on:
    - Amount similarity
    - Customer ID match
    - Settlement time proximity
    """

    score = 0
    reasons = []

    # -------------------------
    # 1. CUSTOMER ID (40 points)
    # -------------------------

    if gateway["customer_id"] == bank["customer_id"]:
        score += 40
        reasons.append("Customer ID matched")
    else:
        reasons.append("Customer ID mismatch")

    # -------------------------
    # 2. AMOUNT (40 points)
    # -------------------------

    amount_difference = abs(
        gateway["amount"] - bank["amount"]
    )

    if amount_difference == 0:
        score += 40
        reasons.append("Exact amount matched")

    elif amount_difference <= 2:
        score += 30
        reasons.append(
            f"Minor amount difference: ₹{amount_difference}"
        )

    elif amount_difference <= 10:
        score += 15
        reasons.append(
            f"Amount difference: ₹{amount_difference}"
        )

    else:
        reasons.append(
            f"Large amount difference: ₹{amount_difference}"
        )

    # -------------------------
    # 3. TIME PROXIMITY (20 points)
    # -------------------------

    gateway_time = datetime.fromisoformat(
        gateway["timestamp"]
    )

    bank_time = datetime.fromisoformat(
        bank["timestamp"]
    )

    time_difference = abs(
        (bank_time - gateway_time).total_seconds()
    ) / 60

    if time_difference <= 60:
        score += 20
        reasons.append(
            f"Settlement within {int(time_difference)} minutes"
        )

    elif time_difference <= 180:
        score += 12
        reasons.append(
            f"Settlement delayed by {int(time_difference)} minutes"
        )

    elif time_difference <= 1440:
        score += 5
        reasons.append(
            f"Settlement delayed by {int(time_difference)} minutes"
        )

    else:
        reasons.append("Settlement time too far apart")

    return score, reasons, time_difference


def find_best_match(gateway_record, bank_records, used_bank_records):
    """
    Find the best possible bank settlement record
    for a gateway transaction.
    """

    best_match = None
    best_score = -1
    best_reasons = []
    best_time_difference = None

    for bank in bank_records:

        bank_reference = bank["bank_reference"]

        if bank_reference in used_bank_records:
            continue

        score, reasons, time_difference = calculate_similarity(
            gateway_record,
            bank
        )

        if score > best_score:

            best_score = score
            best_match = bank
            best_reasons = reasons
            best_time_difference = time_difference

    return (
        best_match,
        best_score,
        best_reasons,
        best_time_difference
    )


def reconcile_transactions():
    """
    Main reconciliation workflow.

    Loads synthetic data, compares transactions,
    assigns confidence-based decisions,
    and returns metrics and audit results.
    """

    start_time = time.time()

    gateway_records = load_json(
        "gateway_transactions.json"
    )

    bank_records = load_json(
        "bank_settlements.json"
    )

    ground_truth = load_json(
        "ground_truth.json"
    )

    truth_lookup = {
        item["transaction_id"]: item
        for item in ground_truth
    }

    used_bank_records = set()

    results = []
    matched_count = 0
    review_count = 0
    unresolved_count = 0

    for gateway in gateway_records:

        (
            best_match,
            confidence,
            reasons,
            time_difference
        ) = find_best_match(
            gateway,
            bank_records,
            used_bank_records
        )

        # -------------------------
        # DECISION ENGINE
        # -------------------------

        if best_match is None or confidence < 50:

            decision = "UNRESOLVED"
            unresolved_count += 1

        elif confidence >= 80:

            decision = "MATCHED"
            matched_count += 1

            used_bank_records.add(
                best_match["bank_reference"]
            )

        else:

            decision = "MANUAL_REVIEW"
            review_count += 1

        # -------------------------
        # AUDIT RESULT
        # -------------------------

        expected = truth_lookup.get(
            gateway["transaction_id"],
            {}
        )

        results.append({
            "transaction_id": gateway["transaction_id"],
            "gateway_amount": gateway["amount"],
            "bank_reference": (
                best_match["bank_reference"]
                if best_match
                else None
            ),
            "bank_amount": (
                best_match["amount"]
                if best_match
                else None
            ),
            "confidence_score": round(confidence, 2),
            "decision": decision,
            "reasons": reasons,
            "time_difference_minutes": (
                round(time_difference, 2)
                if time_difference is not None
                else None
            ),
            "expected_status": expected.get(
                "expected_status"
            ),
            "scenario": expected.get("scenario")
        })

    processing_time = time.time() - start_time

    total_records = len(gateway_records)

    # -------------------------
    # METRICS
    # -------------------------

    correct_decisions = 0

    for result in results:

        expected_status = result["expected_status"]
        actual_decision = result["decision"]

        if expected_status == "MATCHED" and \
                actual_decision in ["MATCHED", "MANUAL_REVIEW"]:

            correct_decisions += 1

        elif expected_status == actual_decision:
            correct_decisions += 1

    accuracy = (
        correct_decisions / total_records * 100
        if total_records > 0
        else 0
    )

    match_rate = (
        matched_count / total_records * 100
        if total_records > 0
        else 0
    )

    throughput = (
        total_records / processing_time
        if processing_time > 0
        else 0
    )

    # -------------------------
    # DUPLICATE SETTLEMENTS
    # -------------------------

    bank_reference_counts = {}

    for bank in bank_records:

        customer_id = bank["customer_id"]

        bank_reference_counts.setdefault(
            customer_id,
            0
        )

        bank_reference_counts[customer_id] += 1

    duplicate_count = len(bank_records) - len(
        used_bank_records
    )

    exceptions = [

        result for result in results

        if result["decision"] in [
            "UNRESOLVED",
            "MANUAL_REVIEW"
        ]
    ]

    return {
        "summary": {
            "total_records": total_records,
            "matched": matched_count,
            "manual_review": review_count,
            "unresolved": unresolved_count,
            "match_rate": round(match_rate, 2),
            "accuracy": round(accuracy, 2),
            "processing_time_seconds": round(
                processing_time,
                4
            ),
            "throughput_records_per_second": round(
                throughput,
                2
            ),
            "duplicate_settlements_detected": duplicate_count
        },
        "results": results,
        "exceptions": exceptions
    }


if __name__ == "__main__":

    reconciliation_result = reconcile_transactions()

    print("\nRECONCILIATION COMPLETED\n")

    print("SUMMARY")

    for key, value in reconciliation_result[
        "summary"
    ].items():

        print(
            f"{key.replace('_', ' ').title()}: "
            f"{value}"
        )

    print("\nSample Results:\n")

    for result in reconciliation_result["results"][:5]:

        print(
            result["transaction_id"],
            "→",
            result["decision"],
            "| Confidence:",
            result["confidence_score"]
        )