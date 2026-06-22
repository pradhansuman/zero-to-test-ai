"""
agents/sdet.py — deprecated shim.
Superseded by agents/designer.py (TestDesignerAgent).
Kept so any lingering `from agents.sdet import SDETAgent` still imports.
"""
from agents.designer import TestDesignerAgent as SDETAgent  # noqa: F401
