def create_action_plan(
    financial_summary,
    prioritized_exceptions
):
    """
    Creates an explainable action plan based on the
    reconciliation batch and priority analysis.
    """

    immediate_actions = []
    monitoring_actions = []
    manual_review_actions = []

    for item in prioritized_exceptions:

        priority = item.get(
            "priority_level",
            "LOW"
        )

        transaction_id = item.get(
            "transaction_id"
        )

        amount_at_risk = item.get(
            "amount_at_risk",
            0
        )

        decision = item.get(
            "decision",
            ""
        )

        recommended_action = item.get(
            "recommended_action",
            "Review transaction details."
        )

        action_item = {
            "transaction_id": transaction_id,
            "amount_at_risk": amount_at_risk,
            "priority_level": priority,
            "recommended_action": recommended_action
        }

        # Critical and high-priority cases
        if priority in ["CRITICAL", "HIGH"]:

            immediate_actions.append(
                action_item
            )

        # Manual review cases
        elif decision == "MANUAL_REVIEW":

            manual_review_actions.append(
                action_item
            )

        # Lower-priority cases
        else:

            monitoring_actions.append(
                action_item
            )


    top_priority = None

    if prioritized_exceptions:

        top_priority = prioritized_exceptions[0]


    # Create executive recommendation
    if top_priority:

        executive_recommendation = (
            f"Prioritize {top_priority['transaction_id']} "
            f"first. It has ₹{top_priority['amount_at_risk']} "
            f"at potential financial risk and is ranked "
            f"#{top_priority['rank']} in the action queue."
        )

    else:

        executive_recommendation = (
            "No financial exceptions require "
            "immediate action."
        )


    return {

        "batch_status": determine_batch_status(
            financial_summary
        ),

        "executive_recommendation":
            executive_recommendation,

        "immediate_actions":
            immediate_actions,

        "monitoring_actions":
            monitoring_actions,

        "manual_review_actions":
            manual_review_actions,

        "total_immediate_actions":
            len(immediate_actions),

        "total_monitoring_actions":
            len(monitoring_actions),

        "total_manual_reviews":
            len(manual_review_actions)

    }


def determine_batch_status(
    financial_summary
):
    """
    Determines the overall health of the
    reconciliation batch.
    """

    total_exceptions = financial_summary.get(
        "total_exceptions",
        0
    )

    critical_cases = financial_summary.get(
        "critical_cases",
        0
    )

    high_priority_cases = financial_summary.get(
        "high_priority_cases",
        0
    )


    if critical_cases > 0:

        return "CRITICAL"

    elif high_priority_cases >= 5:

        return "ATTENTION_REQUIRED"

    elif total_exceptions > 0:

        return "MONITORING"

    return "HEALTHY"