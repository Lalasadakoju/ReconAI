# ReconAI

## AI-Powered Financial Transaction Reconciliation System

ReconAI is an intelligent financial transaction reconciliation system designed to compare payment gateway transactions with bank settlement records.

The system automatically identifies matched transactions, records requiring manual review, and unresolved exceptions. It also provides AI-powered investigation, financial risk prioritization, and recommended actions through an interactive dashboard.

---

## Features

- Automated transaction reconciliation
- Gateway and bank settlement comparison
- Transaction confidence scoring
- Matched, manual review, and unresolved classifications
- AI-powered exception investigation
- Financial risk prioritization
- Recommended action planning
- Financial summary dashboard
- Search and filter transactions
- Exception monitoring
- Audit trail generation
- Responsive user interface

---

## Project Architecture

ReconAI consists of three main components:

### Frontend

The frontend provides an interactive dashboard where users can run reconciliation and view transaction results, exceptions, investigations, priorities, and recommended actions.

Technologies used:

- HTML
- CSS
- JavaScript

### Backend

The backend processes financial transaction data and provides API endpoints for the frontend.

Technologies used:

- Python
- FastAPI
- Pydantic
- Uvicorn

### Data

The system uses JSON datasets representing:

- Payment gateway transactions
- Bank settlement records
- Ground truth data for validation

---

## Project Structure

```text
ReconAI/
│
├── backend/
│   ├── main.py
│   ├── generator.py
│   ├── reconciliation.py
│   ├── investigator.py
│   ├── priority_engine.py
│   ├── action_planner.py
│   └── models.py
│
├── data/
│   ├── gateway_transactions.json
│   ├── bank_settlements.json
│   └── ground_truth.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── README.md
└── requirements.txt