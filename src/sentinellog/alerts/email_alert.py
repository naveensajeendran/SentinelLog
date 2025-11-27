import smtplib
from email.mime.text import MIMEText
from sentinellog.alerts.base import BaseAlert
from sentinellog.core.threats import Threat


class EmailAlert(BaseAlert):
    def __init__(self, smtp_server: str, smtp_port: int, sender: str, recipient: str):
        self.server = smtp_server
        self.port = smtp_port
        self.sender = sender
        self.recipient = recipient

    def send(self, threat: Threat):
        msg = MIMEText(
            f"Threat detected:\n"
            f"Rule: {threat.rule_id}\n"
            f"Level: {threat.level}\n"
            f"Message: {threat.message}\n"
            f"Metadata: {threat.metadata}"
        )

        msg["Subject"] = f"[SentinelLog] {threat.level} Threat"
        msg["From"] = self.sender
        msg["To"] = self.recipient

        try:
            with smtplib.SMTP(self.server, self.port) as smtp:
                smtp.sendmail(self.sender, [self.recipient], msg.as_string())
        except Exception as e:
            print(f"[EmailAlert] Failed: {e}")