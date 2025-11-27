from sentinellog.alerts.base import BaseAlert
from sentinellog.core.threats import Threat


class SlackAlert(BaseAlert):
    def __init__(self, webhook_url: str):
        self.url = webhook_url

    def send(self, threat: Threat):
        payload = {
            "text": (
                f"*SentinelLog Threat Detected*\n"
                f"• *Rule:* {threat.rule_id}\n"
                f"• *Level:* {threat.level}\n"
                f"• *Message:* {threat.message}\n"
                f"• *Metadata:* `{threat.metadata}`"
            )
        }

        try:
            import requests
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "The 'requests' package is required for Slack alerts. "
                "Install it with 'pip install requests'."
            )

        try:
            requests.post(self.url, json=payload)
        except Exception as e:
            print(f"[SlackAlert] Failed: {e}")