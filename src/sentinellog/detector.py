from sentinellog.rules import SecurityRules
from sentinellog.alerts import AlertManager
from sentinellog.parser import LogParser

class ThreatDetector:
    def __init__(self):
        self.rules = SecurityRules()
        self.parser = LogParser()
        self.alerts = AlertManager()

    def scan(self, logfile_path):
        entries = self.parser.parse(logfile_path)
        for entry in entries:
            for rule_name, rule_fn in self.rules.RULES.items():
                if rule_fn(entry):
                    self.alerts.send_alert(rule_name, entry)
