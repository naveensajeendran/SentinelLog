modules = [
    'sentinellog',
    'sentinellog.core',
    'sentinellog.core.detector',
    'sentinellog.core.parser',
    'sentinellog.core.rule_engine',
    'sentinellog.core.threats',
    'sentinellog.rules',
    'sentinellog.api',
    'sentinellog.cli',
    'sentinellog.realtime',
    'sentinellog.alerts.base',
    'sentinellog.alerts.email_alert',
    'sentinellog.alerts.slack_alert',
    'sentinellog.alerts.webhook_alert',
]

import importlib
import os
import sys

# Ensure project `src` directory is on sys.path so imports work when running from project root
THIS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if os.path.isdir(SRC_DIR):
    sys.path.insert(0, SRC_DIR)
else:
    # fallback: add project root
    sys.path.insert(0, PROJECT_ROOT)

for m in modules:
    try:
        importlib.import_module(m)
        print('OK import:', m)
    except Exception as e:
        print('ERROR importing', m, type(e).__name__, e)
