from dataclasses import dataclass
from typing import Dict


@dataclass
class Threat:
    level: str       # INFO / LOW / MEDIUM / HIGH / CRITICAL
    message: str
    rule_id: str
    metadata: Dict