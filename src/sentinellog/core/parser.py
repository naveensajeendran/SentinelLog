from typing import List, Dict


class LogParser:
    """
    Simple line-based parser.
    Each log entry becomes a dict with keys:
    - raw: original line
    - fields: parsed tokens (optional)
    """

    def parse(self, filepath: str) -> List[Dict]:
        entries = []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    entries.append({
                        "raw": line,
                        "fields": self._tokenize(line)
                    })
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {filepath}")

        return entries

    def _tokenize(self, line: str) -> List[str]:
        return line.split()