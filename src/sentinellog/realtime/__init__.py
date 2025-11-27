"""
Real-time components such as filesystem watchers and streaming detection.
"""

from .watcher import FileWatcher

# Backwards compatible alias
LogWatcher = FileWatcher

__all__ = ["FileWatcher", "LogWatcher"]
