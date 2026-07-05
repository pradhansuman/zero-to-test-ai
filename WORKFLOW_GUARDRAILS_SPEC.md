# Workflow Guardrails - REQ-19 - IMPLEMENTED ✅

**Status:** Complete | **Items:** 17 workflow-centric test categories

## Objective
Ensure every business workflow is validated from start to finish rather than testing individual pages or APIs in isolation.

## LLM Responsibilities

| ID | Responsibility | Description |
|----|-----------------|-------------|
| WF-19.1 | Discover workflows | Map all business processes |
| WF-19.2 | Entry points | Identify workflow start conditions |
| WF-19.3 | Exit points | Identify completion conditions |
| WF-19.4 | Alternate paths | Test non-happy-path flows |
| WF-19.5 | Exception paths | Handle error scenarios |
| WF-19.6 | Hidden transitions | Discover state transitions |
| WF-19.7 | Business rules | Validate enforcement |
| WF-19.8 | Missing validations | Identify gaps |
| WF-19.9 | Invalid state transitions | Prevent invalid states |
| WF-19.10 | Race conditions | Test concurrent execution |
| WF-19.11 | Duplicate execution | Verify idempotency |
| WF-19.12 | Rollback validation | Test state recovery |
| WF-19.13 | Compensation logic | Test undo operations |
| WF-19.14 | Approvals | Validate sign-offs |
| WF-19.15 | Escalation paths | Test escalations |
| WF-19.16 | SLA timers | Test timeout handling |
| WF-19.17 | Workflow diagram | Document flow visually |

## Test Categories

- **Happy Path** — Standard workflow execution
- **Negative** — Invalid inputs/states
- **Alternative Path** — Conditional branches
- **Recovery** — Error handling/retry
- **Timeout** — SLA/timeout behavior
- **Duplicate Submission** — Idempotency
- **Concurrency** — Parallel execution
- **Rollback** — State reversal
- **Resume** — Workflow continuation
- **Cancellation** — Workflow termination
- **Interrupted Workflow** — Mid-flow interruption
- **Dependency Failure** — Upstream failures

## Questions to Ask

1. What starts this workflow?
2. Who can start it?
3. Who approves it?
4. Can it be cancelled?
5. Can it resume?
6. Can it rollback?
7. Can two users execute simultaneously?
8. What happens if a dependency fails?
9. Can workflow skip steps?
10. What states exist?

## Deliverables

- **Workflow Diagram** — Visual representation of all flows
- **State Transition Matrix** — Valid state transitions
- **Business Rule Matrix** — Rules enforcement
- **Workflow Test Matrix** — Test coverage per flow
- **Dependency Map** — External dependencies

