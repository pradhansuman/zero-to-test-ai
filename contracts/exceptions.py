"""
contracts/exceptions.py
────────────────────────
Typed exception hierarchy for the QA pipeline.

Catching the right class lets CI and the CLI distinguish recoverable errors
(rate limits, transient 5xx) from permanent failures (bad issue number, broken
LLM contract) and react precisely — retry vs. fail fast vs. notify.

Hierarchy:
    PipelineError
    ├── IngestorError
    │   ├── RateLimitError       — GitHub rate limit hit; retry after reset_at
    │   └── InvalidIssueError    — PR passed as issue, bad repo format
    ├── LLMError                 — model response didn't satisfy the contract
    │   └── TruncatedResponseError — hit token ceiling even after retry
    └── RunnerError              — Playwright workspace or execution failure
"""
from __future__ import annotations


class PipelineError(Exception):
    """Base for all pipeline errors. Catch this to handle any stage failure."""


# ── Ingestor ──────────────────────────────────────────────────────────────────
class IngestorError(PipelineError):
    """GitHub API or issue validation failure."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(IngestorError):
    """GitHub rate limit exceeded. `reset_at` is a Unix timestamp string."""
    def __init__(self, reset_at: str):
        super().__init__(
            f"GitHub rate limit reached — resets at Unix time {reset_at}. "
            f"Add --token ghp_xxx to raise the limit from 60 to 5,000 req/hour.",
            status_code=403,
        )
        self.reset_at = reset_at


class InvalidIssueError(IngestorError):
    """The reference points to something that isn't a usable issue."""
    pass


# ── LLM agents ────────────────────────────────────────────────────────────────
class LLMError(PipelineError):
    """An LLM agent failed to produce a valid contract from the model response."""
    def __init__(self, agent_name: str, message: str):
        super().__init__(f"[{agent_name}] {message}")
        self.agent_name = agent_name


class TruncatedResponseError(LLMError):
    """Response hit the token ceiling even after retry with doubled budget."""
    def __init__(self, agent_name: str, budget: int):
        super().__init__(
            agent_name,
            f"Output exceeded {budget} tokens after retry. "
            f"Split the issue or lower the scenario count.",
        )
        self.budget = budget


# ── Runner ────────────────────────────────────────────────────────────────────
class RunnerError(PipelineError):
    """Playwright workspace setup or test execution failure."""
    def __init__(self, message: str, exit_code: int | None = None):
        super().__init__(message)
        self.exit_code = exit_code
