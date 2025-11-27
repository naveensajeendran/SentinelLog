from sentinellog.alerts.base import BaseAlert
from sentinellog.core.threats import Threat


class WebhookAlert(BaseAlert):
    def __init__(self, url: str):
        self.url = url

    def send(self, threat: Threat):
        data = {
            "rule_id": threat.rule_id,
            "level": threat.level,
            "message": threat.message,
            "metadata": threat.metadata
        }

        try:
            import requests
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "The 'requests' package is required for Webhook alerts. "
                "Install it with 'pip install requests'."
            )

        try:
            requests.post(self.url, json=data)
        except Exception as e:
            print(f"[WebhookAlert] Failed: {e}")