from sentinellog.detector import ThreatDetector

def test_failed_login_detection():
    detector = ThreatDetector()
    logs = ["Failed password for root"]
    results = detector.run(logs)
    assert len(results) == 1
    assert results[0]["rule"] == "FAILED_LOGIN"
