import yaml
from sentinellog.core.rule_engine import RuleEngine
from sentinellog.core.threats import Threat


def test_rule_engine_matches_pattern(tmp_path):
    rules = [
        {"id": "TEST_1", "pattern": "Failed password", "level": "HIGH"},
        {"id": "TEST_2", "pattern": "Accepted password", "level": "LOW"},
    ]
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text(yaml.safe_dump(rules), encoding="utf-8")

    engine = RuleEngine(str(rules_file))

    entry = {"raw": "Nov 22 Failed password for root"}
    threats = engine.evaluate(entry)

    assert isinstance(threats, list)
    assert all(isinstance(t, Threat) for t in threats)
    assert any(t.rule_id == "TEST_1" for t in threats)
