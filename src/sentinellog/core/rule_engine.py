import yaml
from typing import List, Dict
from sentinellog.core.threats import Threat


class RuleEngine:
    """
    Loads YAML rules and matches log lines.
    YAML structure:
      - id: BRUTE_FORCE_1
        pattern: "Failed password"
        level: HIGH
        metadata:
            source: auth_log
    """

    def __init__(self, rules_path: str):
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Dict]:
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or []
        except FileNotFoundError:
            # No rules file provided or found; return empty ruleset
            return []

    def evaluate(self, entry) -> List[Threat]:
        """Evaluate a single entry and return list of Threat objects.

        `entry` may be a dict with a `raw` key or a plain string.
        """
        threats = []
        if isinstance(entry, dict):
            text = entry.get("raw", "")
        else:
            text = str(entry)

        for r in self.rules:
            pattern = str(r.get("pattern", ""))
            if pattern and pattern.lower() in text.lower():
                threats.append(
                    Threat(
                        level=r.get("level", "INFO"),
                        message=f"Matched rule: {r.get('id')}",
                        rule_id=r.get("id", ""),
                        metadata=r.get("metadata", {})
                    )
                )

        return threats