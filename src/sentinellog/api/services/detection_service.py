from sentinellog.core.detector import ThreatDetector
from sentinellog.core.rule_engine import RuleEngine


class DetectionService:
    def __init__(self, rules_path: str):
        self.rules_path = rules_path
        self.detector = ThreatDetector(rules_path)

    def scan_file(self, path: str):
        return self.detector.scan(path)

    def scan_text(self, text: str):
        threats = []
        for line in text.split("\n"):
            if line.strip():  # Skip empty lines
                entry = {"raw": line, "fields": line.split()}
                threats.extend(self.detector.engine.evaluate(entry))
        return threats

    def reload_rules(self):
        """Reload rules from disk without restarting service."""
        try:
            # Recreate the engine with fresh rules
            self.detector.engine = RuleEngine(self.rules_path)
        except Exception as e:
            raise RuntimeError(f"Failed to reload rules: {str(e)}")

    def list_rules(self):
        return self.detector.engine.rules
