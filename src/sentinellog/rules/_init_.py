"""
Rules module for SentinelLog.
Loads YAML rule definitions for threat detection.
"""

from .rules_loader import load_rules

__all__ = ["load_rules"]
