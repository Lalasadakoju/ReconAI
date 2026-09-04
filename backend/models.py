from typing import List, Optional
from pydantic import BaseModel


class ReconciliationSummary(BaseModel):
    total_records: int
    matched: int
    manual_review: int
    unresolved: int
    match_rate: float
    accuracy: float
    processing_time_seconds: float
    throughput_records_per_second: float
    duplicate_settlements_detected: int


class ReconciliationResult(BaseModel):
    transaction_id: str
    gateway_amount: float
    bank_reference: Optional[str] = None
    bank_amount: Optional[float] = None
    confidence_score: float
    decision: str
    reasons: List[str]
    time_difference_minutes: Optional[float] = None
    expected_status: Optional[str] = None
    scenario: Optional[str] = None


class ReconciliationResponse(BaseModel):
    summary: ReconciliationSummary
    results: List[ReconciliationResult]
    exceptions: List[ReconciliationResult]