import os
from sentinellog.detector import ThreatDetector

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logfile = os.path.join(base_dir, "..", "..", "logs", "sample.log")
    logfile = os.path.abspath(logfile)

    detector = ThreatDetector()
    detector.scan(logfile)

if __name__ == "__main__":
    main()
