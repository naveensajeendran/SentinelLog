class AlertManager:
    def send_alert(self, rule_name, entry):
        print(f"[ALERT] Rule triggered: {rule_name} -> {entry}")
