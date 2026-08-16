"""Small policy engine used by the secure-agent demo."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    requires_approval: bool = False


class PolicyEngine:
    """Enforce capabilities before a tool is executed."""

    def __init__(self) -> None:
        self.allowed_tools = {
            "read_package",
            "search_cves",
            "get_report",
        }
        self.approval_tools = {"export_report"}
        self.denied_tools = {
            "write_database",
            "delete_record",
            "run_shell",
        }

    def evaluate(self, tool: str, arguments: dict[str, Any] | None = None) -> Decision:
        arguments = arguments or {}

        if tool in self.denied_tools:
            return Decision(False, f"{tool} is explicitly denied")

        if tool in self.approval_tools:
            return Decision(False, f"{tool} requires human approval", requires_approval=True)

        if tool not in self.allowed_tools:
            return Decision(False, f"{tool} is not present in the allowlist")

        return Decision(True, "allowed by policy")
