"""Minimal Human-in-the-Loop approval gate for demo-sensitive actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalResult:
    approved: bool
    reason: str


def request_approval(tool: str, arguments: dict) -> ApprovalResult:
    """Ask a human to approve a sensitive action before execution.

    This is intentionally a CLI demo gate, not a production approval system.
    """
    print("\n👤 HUMAN APPROVAL REQUIRED")
    print(f"tool: {tool}")
    print(f"arguments: {arguments}")
    answer = input("Approve action? [y/N]: ").strip().lower()

    if answer in {"y", "yes"}:
        return ApprovalResult(True, "approved by human")

    return ApprovalResult(False, "rejected by human")
