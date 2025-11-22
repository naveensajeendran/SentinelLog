class LogParser:
    def parse(self, filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]
