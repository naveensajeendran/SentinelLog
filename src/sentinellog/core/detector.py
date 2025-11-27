from typing import List, Optional
from sentinellog.core.parser import LogParser
from sentinellog.core.rule_engine import RuleEngine
from sentinellog.core.threats import Threat
from sentinellog.core.utils import resolve_path


class ThreatDetector:
    """High-level engine that parses logs, applies rules, and returns Threats.

    The detector accepts an optional `rules_path`. If not provided, it will
    look for `rules.yaml` in the project `rules/` directory.
    """

    def __init__(self, rules_path: Optional[str] = None):
        self.parser = LogParser()
        if rules_path is None:
            # default rules path under project root
            rules_path = resolve_path("rules", "rules.yaml")
        self.engine = RuleEngine(rules_path)

    def scan(self, logfile: str) -> List[Threat]:
        entries = self.parser.parse(logfile)
        return self.run(entries)

    def run(self, entries) -> List[Threat]:
        """Evaluate a list of entries (strings or dicts) and return Threats."""
        threats: List[Threat] = []
        for entry in entries:
            threats.extend(self.engine.evaluate(entry))
        return threats