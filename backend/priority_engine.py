def calculate_financial_impact(transaction):
    """
    Calculates the amount of money associated with
    a reconciliation exception.
    """

    gateway_amount = transaction.get(
        "gateway_amount",
        0
    )

    bank_amount = transaction.get(
        "bank_amount"
    )

    # If bank settlement exists, calculate the difference.
    if bank_amount is not None:

        amount_difference = abs(
            gateway_amount - bank_amount
        )

        # For delayed or uncertain settlements,
        # the full transaction amount is considered at risk.
        if amount_difference == 0:
            amount_at_risk = gateway_amount
        else:
            amount_at_risk = amount_difference

    else:

        # Missing settlement means the full amount is at risk.
        amount_at_risk = gateway_amount

    return round(amount_at_risk, 2)

def calculate_priority_score(
    transaction,
    investigation
):
    """
    Calculates an explainable priority score.

    The score considers financial impact, risk,
    reconciliation status and confidence.
    """

    score = 0

    amount_at_risk = calculate_financial_impact(
        transaction
    )

    # -----------------------------------
    # FINANCIAL IMPACT — maximum 45 points
    # -----------------------------------

    if amount_at_risk >= 50000:

        financial_score = 45

    else:

        # Dynamic scaling for smaller amounts
        financial_score = (
            amount_at_risk / 50000
        ) * 45


    score += financial_score


    # -----------------------------------
    # RISK LEVEL — maximum 25 points
    # -----------------------------------

    risk_level = investigation.get(
        "risk_level",
        "LOW"
    )

    if risk_level == "HIGH":

        score += 25

    elif risk_level == "MEDIUM":

        score += 15

    else:

        score += 5


    # -----------------------------------
    # DECISION SEVERITY — maximum 20 points
    # -----------------------------------

    decision = transaction.get(
        "decision"
    )

    if decision == "UNRESOLVED":

        score += 20

    elif decision == "MANUAL_REVIEW":

        score += 10


    # -----------------------------------
    # CONFIDENCE PENALTY — maximum 10 points
    # -----------------------------------

    confidence = transaction.get(
        "confidence_score",
        100
    )

    if confidence < 50:

        score += 10

    elif confidence < 80:

        score += 5


    return round(
        min(score, 100),
        2
    )

def get_priority_level(score):
    """
    Converts a numerical priority score into
    a human-readable priority level.
    """

    if score >= 75:
        return "CRITICAL"

    elif score >= 55:
        return "HIGH"

    elif score >= 35:
        return "MEDIUM"

    return "LOW"


def prioritize_exceptions(
    exceptions,
    investigations
):
    """
    Combines reconciliation data and investigation
    results, then ranks exceptions by urgency.
    """

    prioritized = []

    # Create quick lookup for investigations
    investigation_map = {
        item["transaction_id"]: item
        for item in investigations
    }


    for transaction in exceptions:

        transaction_id = transaction.get(
            "transaction_id"
        )

        investigation = investigation_map.get(
            transaction_id,
            {}
        )

        amount_at_risk = calculate_financial_impact(
            transaction
        )

        priority_score = calculate_priority_score(
            transaction,
            investigation
        )

        priority_level = get_priority_level(
            priority_score
        )

        prioritized.append({

            "transaction_id": transaction_id,

            "decision": transaction.get("decision"),

            "gateway_amount": transaction.get(
                "gateway_amount"
            ),

            "amount_at_risk": amount_at_risk,

            "priority_score": priority_score,

            "priority_level": priority_level,

            "risk_level": investigation.get(
                "risk_level"
            ),

            "probable_cause": investigation.get(
                "probable_cause"
            ),

            "recommended_action": investigation.get(
                "recommended_action"
            )

        })


    # Highest priority first
    prioritized.sort(
        key=lambda item: item[
            "priority_score"
        ],
        reverse=True
    )


    # Add ranking
    for index, item in enumerate(
        prioritized,
        start=1
    ):

        item["rank"] = index


    return prioritized


def create_financial_summary(
    reconciliation_result,
    prioritized_exceptions
):
    """
    Creates a financial impact summary
    for the entire reconciliation batch.
    """

    results = reconciliation_result.get(
        "results",
        []
    )

    total_processed_amount = sum(
        transaction.get(
            "gateway_amount",
            0
        )
        for transaction in results
    )


    matched_amount = sum(
        transaction.get(
            "gateway_amount",
            0
        )
        for transaction in results
        if transaction.get("decision") == "MATCHED"
    )


    amount_under_review = sum(
        item["amount_at_risk"]
        for item in prioritized_exceptions
        if item["priority_level"]
        in ["MEDIUM", "HIGH"]
    )


    critical_amount_at_risk = sum(
        item["amount_at_risk"]
        for item in prioritized_exceptions
        if item["priority_level"] == "CRITICAL"
    )


    return {

        "total_processed_amount":
            round(total_processed_amount, 2),

        "successfully_reconciled_amount":
            round(matched_amount, 2),

        "amount_under_review":
            round(amount_under_review, 2),

        "critical_amount_at_risk":
            round(critical_amount_at_risk, 2),

        "total_exceptions":
            len(prioritized_exceptions),

        "critical_cases":
            len([
                item
                for item in prioritized_exceptions
                if item["priority_level"]
                == "CRITICAL"
            ]),

        "high_priority_cases":
            len([
                item
                for item in prioritized_exceptions
                if item["priority_level"]
                in ["CRITICAL", "HIGH"]
            ])

    }