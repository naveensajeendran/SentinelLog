"""
Core logic for SentinelLog.
Handles detection, parsing, threat evaluation, and utility functions.
"""

from .detector import ThreatDetector
from .parser import LogParser
from .rule_engine import RuleEngine
from .utils import normalize_text

__all__ = [
    "ThreatDetector",
    "LogParser",
    "RuleEngine",
    "normalize_text"
]
