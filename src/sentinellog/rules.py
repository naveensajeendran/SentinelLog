class SecurityRules:
    def __init__(self):
        self.RULES = {
            "FAILED_LOGIN": self.failed_login,
            "SUSPICIOUS_IP": self.suspicious_ip,
        }

    def failed_login(self, entry):
        return "Failed password" in entry

    def suspicious_ip(self, entry):
        blacklist = ["185.", "45.146."]
        return any(ip in entry for ip in blacklist)
