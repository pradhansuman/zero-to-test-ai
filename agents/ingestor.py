"""
agents/ingestor.py
──────────────────
STAGE 1 — GitHub Issue Ingestion.

This agent is deterministic — it does NOT call the LLM. It hits the real
GitHub REST API, pulls the issue, and normalises it into an IssuePayload that
every downstream agent can rely on.

I/O CONTRACT
    in : IssueRef(repo, issue_number, github_token?)
    out: IssuePayload

Why no LLM here: ingestion must be exact and cheap. Inferring priority from
labels is rule-based and auditable; we don't want a model hallucinating an
issue number or inventing a label.
"""
from __future__ import annotations

import re
import time
import requests

from contracts.schemas import IssueRef, IssuePayload, Priority

GITHUB_API = "https://api.github.com"

# label → priority precedence (first match wins)
_PRIORITY_MAP = {
    r"\bp0\b|critical|blocker": Priority.P0,
    r"\bp1\b|high":             Priority.P1,
    r"\bp2\b|medium|low":       Priority.P2,
}


def _infer_priority(labels: list[str]) -> Priority:
    joined = " ".join(labels).lower()
    for pattern, pri in _PRIORITY_MAP.items():
        if re.search(pattern, joined):
            return pri
    return Priority.P2


def _infer_type(labels: list[str]) -> str:
    joined = " ".join(labels).lower()
    if "bug" in joined or "defect" in joined:
        return "bug"
    if "feature" in joined or "enhancement" in joined:
        return "feature"
    return "chore"


def _infer_component(labels: list[str]) -> str | None:
    # convention: labels like "area:auth" or "component/checkout"
    for lab in labels:
        m = re.match(r"(?:area|component)[:/](.+)", lab.lower())
        if m:
            return m.group(1)
    return None


def _get_with_retry(url: str, headers: dict, retries: int = 3) -> requests.Response:
    """GET with exponential backoff on transient 5xx errors."""
    for attempt in range(retries):
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code < 500:
            return resp                          # success or a client error — stop retrying
        if attempt < retries - 1:
            time.sleep(2 ** attempt)            # 1 s → 2 s → 4 s
    return resp                                 # return last response; caller handles it


def _fetch_top_comments(url: str, headers: dict, limit: int = 5) -> str:
    """Fetch the first `limit` issue comments and return them as a single string."""
    resp = requests.get(url, headers=headers, timeout=20, params={"per_page": limit})
    if not resp.ok:
        return ""
    return "\n\n".join(
        c["body"].strip() for c in resp.json() if c.get("body", "").strip()
    )


class IngestorAgent:
    NAME = "ingestor"

    def run(self, ref: IssueRef) -> IssuePayload:
        # ── GUARD 1: validate repo format ────────────────────────────────────
        if ref.repo.count("/") != 1:
            raise ValueError(
                f"repo must be 'owner/name' (e.g. facebook/react), got: '{ref.repo}'"
            )

        headers = {"Accept": "application/vnd.github+json"}
        if ref.github_token:
            headers["Authorization"] = f"Bearer {ref.github_token}"

        # ── Fetch issue with retry on transient failures ──────────────────────
        url  = f"{GITHUB_API}/repos/{ref.repo}/issues/{ref.issue_number}"
        resp = _get_with_retry(url, headers)

        # ── GUARD 2: surface rate-limit errors with actionable message ────────
        if resp.status_code == 403 and (
            "rate limit" in resp.text.lower() or
            resp.headers.get("X-RateLimit-Remaining") == "0"
        ):
            reset = resp.headers.get("X-RateLimit-Reset", "unknown")
            raise RuntimeError(
                f"GitHub rate limit reached (resets at Unix time {reset}). "
                f"Add --token ghp_xxx to raise the limit from 60 to 5,000 requests/hour."
            )

        resp.raise_for_status()
        data = resp.json()

        # ── GUARD 3: reject Pull Requests passed as issue numbers ─────────────
        if "pull_request" in data:
            raise ValueError(
                f"#{ref.issue_number} is a Pull Request, not an Issue. "
                f"Please provide a GitHub Issue number."
            )

        labels = [l["name"] for l in data.get("labels", [])]

        # ── Fetch top comments for richer PlannerAgent context ────────────────
        comments_text = ""
        if data.get("comments", 0) > 0:
            comments_url = f"{GITHUB_API}/repos/{ref.repo}/issues/{ref.issue_number}/comments"
            comments_text = _fetch_top_comments(comments_url, headers)

        body = (data.get("body") or "").strip()
        if comments_text:
            body = f"{body}\n\n---\nTOP COMMENTS:\n{comments_text}"

        return IssuePayload(
            issue_number=data["number"],
            repo=ref.repo,
            state=data.get("state", "open"),
            title=data.get("title", ""),
            body=body,
            labels=labels,
            priority=_infer_priority(labels),
            type=_infer_type(labels),
            component=_infer_component(labels),
            milestone=(data.get("milestone") or {}).get("title"),
            author=(data.get("user") or {}).get("login"),
            comments_count=data.get("comments", 0),
            url=data.get("html_url", ""),
            pipeline_stage="ingested",
            ready_for_planner=True,
        )
