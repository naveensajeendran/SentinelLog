from sentinellog.core.detector import ThreatDetector
import yaml


def test_core_detector_run_returns_threats(tmp_path):
    rules = [
        {"id": "FAILED_LOGIN", "pattern": "Failed password", "level": "HIGH"}
    ]
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text(yaml.safe_dump(rules), encoding="utf-8")

    detector = ThreatDetector(str(rules_file))
    entries = [{"raw": "Nov 22 Failed password for root"}]

    threats = detector.run(entries)

    assert isinstance(threats, list)
    assert len(threats) == 1
    t = threats[0]
    assert hasattr(t, "rule_id")
    assert t.rule_id == "FAILED_LOGIN"
