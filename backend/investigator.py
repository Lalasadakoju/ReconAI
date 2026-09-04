def investigate_transaction(transaction):
    """
    Investigates a reconciliation exception and generates
    an explainable financial operations recommendation.
    """

    decision = transaction.get("decision")
    confidence = transaction.get("confidence_score", 0)
    time_difference = transaction.get(
        "time_difference_minutes"
    )
    gateway_amount = transaction.get(
        "gateway_amount"
    )
    bank_amount = transaction.get("bank_amount")

    probable_cause = ""
    risk_level = ""
    recommended_action = ""

    # Missing settlement
    if (
        decision == "UNRESOLVED"
        and transaction.get("bank_reference") is None
    ):
        probable_cause = (
            "No corresponding bank settlement was "
            "identified for this gateway transaction."
        )

        risk_level = "HIGH"

        recommended_action = (
            "Verify whether the bank settlement is delayed. "
            "Check settlement reports before escalating "
            "the transaction."
        )

    # Large settlement delay
    elif (
        time_difference is not None
        and time_difference > 180
    ):
        probable_cause = (
            "The settlement timing differs significantly "
            "from the original transaction time."
        )

        risk_level = "MEDIUM"

        recommended_action = (
            "Verify the bank processing window and confirm "
            "whether delayed settlement is expected."
        )

    # Amount mismatch
    elif (
        gateway_amount is not None
        and bank_amount is not None
        and gateway_amount != bank_amount
    ):
        difference = abs(
            gateway_amount - bank_amount
        )

        probable_cause = (
            f"Gateway and bank amounts differ by "
            f"₹{difference}."
        )

        risk_level = "MEDIUM"

        recommended_action = (
            "Verify fees, adjustments, refunds, or partial "
            "settlements before approving the match."
        )

    # Low confidence
    elif confidence < 80:
        probable_cause = (
            "The available evidence is insufficient for "
            "a high-confidence automatic reconciliation."
        )

        risk_level = "MEDIUM"

        recommended_action = (
            "Review transaction identifiers and settlement "
            "details manually."
        )

    # Fallback
    else:
        probable_cause = (
            "The transaction contains inconsistent "
            "reconciliation signals."
        )

        risk_level = "LOW"

        recommended_action = (
            "Review the transaction and supporting "
            "settlement records."
        )

    return {
        "transaction_id": transaction.get(
            "transaction_id"
        ),
        "decision": decision,
        "confidence_score": confidence,
        "probable_cause": probable_cause,
        "risk_level": risk_level,
        "recommended_action": recommended_action
    }


def investigate_exceptions(exceptions):
    """
    Investigate all reconciliation exceptions.
    """

    investigations = []

    for transaction in exceptions:

        investigation = investigate_transaction(
            transaction
        )

        investigations.append(investigation)

    return investigations