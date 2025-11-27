from pydantic import BaseModel
from typing import List, Optional

class LogEntry(BaseModel):
    timestamp: str
    source: str
    message: str
    raw: Optional[str] = None

class ThreatResult(BaseModel):
    threat_type: str
    severity: str
    description: str
    matched_rule: Optional[str] = None
    line_number: Optional[int] = None

class ScanResponse(BaseModel):
    file_scanned: str
    threats_found: int
    results: List[ThreatResult]

class APIStatus(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    message: str = "SentinelLog API is running"