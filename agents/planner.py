"""
agents/planner.py — deprecated shim.
Superseded by agents/strategist.py (StrategistAgent).
Kept so any lingering `from agents.planner import PlannerAgent` still imports.
"""
from agents.strategist import StrategistAgent as PlannerAgent  # noqa: F401
