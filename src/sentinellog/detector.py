"""Compatibility wrapper for ThreatDetector.

Provides a backward-compatible `ThreatDetector` with `run(entries)` and
`scan(logfile)` methods that match the older test expectations. If a
`rules_path` is provided to the constructor, the wrapper will delegate to
the refactored core detector.
"""
from typing import List

try:
	from sentinellog.core.detector import ThreatDetector as CoreThreatDetector
except Exception:
	CoreThreatDetector = None


class SecurityRules:
	def __init__(self):
		self.RULES = {
			"FAILED_LOGIN": self.failed_login,
			"SUSPICIOUS_IP": self.suspicious_ip,
		}

	def failed_login(self, entry: str) -> bool:
		return "Failed password" in entry

	def suspicious_ip(self, entry: str) -> bool:
		blacklist = ["185.", "45.146."]
		return any(ip in entry for ip in blacklist)


class ThreatDetector:
	"""Compatibility ThreatDetector.

	- `ThreatDetector()` (no args) provides a `run(entries: List[str])` method
	  that returns a list of dicts like `{"rule": RULE_NAME, "entry": entry}`.
	- `ThreatDetector(rules_path)` delegates to the core detector if
	  available and converts results to the legacy dict format where needed.
	"""

	def __init__(self, rules_path: str = None):
		if rules_path and CoreThreatDetector is not None:
			self._core = CoreThreatDetector(rules_path)
		else:
			self._core = None
			self.rules = SecurityRules()

	def run(self, entries: List[str]):
		results = []
		if self._core is not None:
			# Core may return Threat dataclasses; convert into legacy dicts
			threats = self._core.run(entries) if hasattr(self._core, "run") else self._core.scan(entries)
			for t in threats:
				rule = getattr(t, "rule_id", getattr(t, "rule", None) or "UNKNOWN")
				entry_text = getattr(t, "message", getattr(t, "entry", ""))
				results.append({"rule": rule, "entry": entry_text})
			return results

		for entry in entries:
			for rule_name, rule_fn in self.rules.RULES.items():
				try:
					if rule_fn(entry):
						results.append({"rule": rule_name, "entry": entry})
				except Exception:
					# Ignore rule errors for compatibility
					continue

		return results

	def scan(self, logfile_path: str):
		if self._core is not None:
			threats = self._core.scan(logfile_path)
			# convert to legacy dicts
			results = []
			for t in threats:
				rule = getattr(t, "rule_id", getattr(t, "rule", None) or "UNKNOWN")
				entry_text = getattr(t, "message", getattr(t, "entry", ""))
				results.append({"rule": rule, "entry": entry_text})
			return results

		# legacy behavior: read lines and run
		with open(logfile_path, "r", encoding="utf-8") as f:
			lines = [line.strip() for line in f if line.strip()]
		return self.run(lines)


__all__ = ["ThreatDetector"]
