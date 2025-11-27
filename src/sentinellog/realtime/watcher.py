import time
import os
from typing import Callable
from sentinellog.core.detector import ThreatDetector


class FileWatcher:
    """
    Tails a file in real time and triggers callback when threats appear.
    """

    def __init__(self, logfile: str, detector: ThreatDetector, callback: Callable):
        self.logfile = logfile
        self.detector = detector
        self.callback = callback

    def start(self):
        print(f"[SentinelLog] Watching {self.logfile}...")

        with open(self.logfile, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()

                if not line:
                    time.sleep(0.5)
                    continue

                entry = {"raw": line.strip(), "fields": line.split()}
                threats = self.detector.engine.evaluate(entry)

                for t in threats:
                    self.callback(t)