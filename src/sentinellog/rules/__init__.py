"""
Rules module for SentinelLog.
Provides a simple `load_rules()` helper that loads YAML rules if present.
"""
import os
import yaml
from typing import List, Dict


def load_rules(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


__all__ = ["load_rules"]
