"""Temporal host for the Life Sciences supervisor agent (spike)."""

import os
import sys

# agent_factory and shared.* live under apps/api and import each other as
# top-level modules; make them importable the same way lifesciences.py does.
_API_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api")
if _API_DIR not in sys.path:
    sys.path.append(_API_DIR)
