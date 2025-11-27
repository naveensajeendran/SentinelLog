from sentinellog.core.parser import LogParser


def test_parse_returns_structured_entries(tmp_path):
    log_content = """
Nov 22 10:00:00 server sshd[12345]: Failed password for invalid user admin from 185.100.87.123 port 22 ssh2
Nov 22 10:01:00 server sshd[12346]: Accepted password for user1 from 192.168.1.10 port 22 ssh2
"""
    p = tmp_path / "sample.log"
    p.write_text(log_content, encoding="utf-8")

    parser = LogParser()
    entries = parser.parse(str(p))

    assert isinstance(entries, list)
    assert len(entries) == 2
    assert isinstance(entries[0], dict)
    assert "raw" in entries[0]
    assert "fields" in entries[0]
    assert "Failed password" in entries[0]["raw"]
