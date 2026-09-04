from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.reconciliation import reconcile_transactions
from backend.generator import generate_synthetic_data
from backend.investigator import investigate_exceptions
from backend.priority_engine import (
    prioritize_exceptions,
    create_financial_summary
)
from backend.models import ReconciliationResponse
from backend.action_planner import create_action_plan

app = FastAPI(
    title="ReconAI API",
    description="AI-Powered Financial Reconciliation Agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "ReconAI API is running successfully!"
    }


@app.post("/generate-data")
def generate_data():
    result = generate_synthetic_data()

    return {
        "message": "Synthetic financial data generated successfully!",
        "details": result
    }


@app.get(
    "/reconcile",
    response_model=ReconciliationResponse
)
def run_reconciliation():

    return reconcile_transactions()


@app.get("/investigate")
def investigate():

    reconciliation_result = reconcile_transactions()

    exceptions = reconciliation_result[
        "exceptions"
    ]

    investigations = investigate_exceptions(
        exceptions
    )

    return {
        "total_exceptions": len(exceptions),
        "investigations": investigations
    }

@app.get("/priorities")
def get_priorities():

    # Step 1: Run reconciliation
    reconciliation_result = reconcile_transactions()

    # Step 2: Get exceptions
    exceptions = reconciliation_result[
        "exceptions"
    ]

    # Step 3: Investigate exceptions
    investigations = investigate_exceptions(
        exceptions
    )

    # Step 4: Rank exceptions
    prioritized_exceptions = prioritize_exceptions(
        exceptions,
        investigations
    )

    # Step 5: Create batch financial summary
    financial_summary = create_financial_summary(
        reconciliation_result,
        prioritized_exceptions
    )

    return {

        "financial_summary":
            financial_summary,

        "prioritized_exceptions":
            prioritized_exceptions

    }

@app.get("/action-plan")
def get_action_plan():

    # Step 1: Run reconciliation
    reconciliation_result = reconcile_transactions()

    # Step 2: Get exceptions
    exceptions = reconciliation_result[
        "exceptions"
    ]

    # Step 3: Investigate exceptions
    investigations = investigate_exceptions(
        exceptions
    )

    # Step 4: Prioritize exceptions
    prioritized_exceptions = prioritize_exceptions(
        exceptions,
        investigations
    )

    # Step 5: Create financial summary
    financial_summary = create_financial_summary(
        reconciliation_result,
        prioritized_exceptions
    )

    # Step 6: Generate action plan
    action_plan = create_action_plan(
        financial_summary,
        prioritized_exceptions
    )

    return action_plan

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ReconAI"
    }