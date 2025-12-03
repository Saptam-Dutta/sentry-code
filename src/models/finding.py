from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Severity(str, Enum):
    CRITICAL = 'CRITICAL'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class Finding(BaseModel):
    rule_id: str
    rule_name: str
    severity: Severity
    cwe_id: str
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    explanation: Optional[str] = None
    impact: Optional[str] = None
    remediation_steps: Optional[List[str]] = None
    fixed_code: Optional[str] = None
    confidence: Optional[float] = None

class ScanResult(BaseModel):
    total_findings: int
    findings: List[Finding]
    files_scanned: int
    severity_counts: dict
