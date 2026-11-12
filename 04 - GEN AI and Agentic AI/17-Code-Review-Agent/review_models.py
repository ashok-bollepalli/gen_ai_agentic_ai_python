from typing import Literal
from pydantic import BaseModel, Field


Severity = Literal["critical", "high", "medium", "low", "info"]


class Finding(BaseModel):
    title: str = Field(description="Short finding title")
    severity: Severity
    category: str = Field(description="bug, security, maintainability, performance, or testing")
    file: str = Field(default="submitted_code.py")
    line: int | None = None
    explanation: str
    recommendation: str
    evidence: str = Field(description="Short source snippet or explanation supporting the finding")


class AIReview(BaseModel):
    summary: str
    findings: list[Finding]
    strengths: list[str] = []
    assumptions: list[str] = []


class TestSuggestions(BaseModel):
    testing_notes: list[str]
    pytest_code: str
