import sys
from sentinellog.alerts.email_alert import EmailAlert
from sentinellog.alerts.slack_alert import SlackAlert
from sentinellog.alerts.webhook_alert import WebhookAlert
from sentinellog.core.threats import Threat


def test_email_alert_sends_email(monkeypatch):
    sent = {}

    class FakeSMTP:
        def __init__(self, server, port):
            sent['server'] = server
            sent['port'] = port
            self.sent_messages = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def sendmail(self, sender, recipients, message):
            sent['sender'] = sender
            sent['recipients'] = recipients
            sent['message'] = message

    monkeypatch.setattr('smtplib.SMTP', FakeSMTP)

    alert = EmailAlert('smtp.example.test', 25, 'from@example.test', 'to@example.test')
    threat = Threat(level='HIGH', message='Test', rule_id='RULE1', metadata={})
    alert.send(threat)

    assert sent['server'] == 'smtp.example.test'
    assert sent['port'] == 25
    assert 'from@example.test' in sent['sender']
    assert 'to@example.test' in sent['recipients'][0]
    assert 'Test' in sent['message']


def test_slack_and_webhook_use_requests(monkeypatch):
    calls = []

    class FakeResp:
        status_code = 200

    def fake_post(url, json=None, **kwargs):
        calls.append((url, json))
        return FakeResp()

    import types
    fake_requests = types.SimpleNamespace(post=fake_post)
    monkeypatch.setitem(sys.modules, 'requests', fake_requests)

    slack = SlackAlert('https://hooks.slack.test/abc')
    webhook = WebhookAlert('https://webhook.test/ingest')

    threat = Threat(level='LOW', message='SlackTest', rule_id='RULE2', metadata={'k': 'v'})

    slack.send(threat)
    webhook.send(threat)

    assert len(calls) == 2
    assert calls[0][0] == 'https://hooks.slack.test/abc'
    assert 'SlackTest' in calls[0][1]['text']
    assert calls[1][0] == 'https://webhook.test/ingest'
    assert calls[1][1]['rule_id'] == 'RULE2'
