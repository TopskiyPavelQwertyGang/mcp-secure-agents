"""Policy-as-code engine used by the secure-agent demo."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_POLICY = Path(__file__).parent / "policies" / "agent-policy.yaml"


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    requires_approval: bool = False


class PolicyEngine:
    """Load policy from YAML and enforce capabilities before tool execution."""

    def __init__(self, policy_path: str | Path = DEFAULT_POLICY) -> None:
        self.policy_path = Path(policy_path)
        data = yaml.safe_load(self.policy_path.read_text(encoding="utf-8")) or {}

        self.mode = data.get("mode", "deny-by-default")
        if self.mode != "deny-by-default":
            raise ValueError(f"Unsupported policy mode: {self.mode}")

        self.allowed_tools = set(data.get("allowed_tools", []))
        self.approval_tools = set(data.get("human_approval", []))
        self.denied_tools = set(data.get("denied_tools", []))
        self.principles = tuple(data.get("principles", []))

        overlap = (
            (self.allowed_tools & self.approval_tools)
            | (self.allowed_tools & self.denied_tools)
            | (self.approval_tools & self.denied_tools)
        )
        if overlap:
            raise ValueError(f"Policy contains conflicting tool rules: {sorted(overlap)}")

    def evaluate(self, tool: str, arguments: dict[str, Any] | None = None) -> Decision:
        _ = arguments or {}

        if tool in self.denied_tools:
            return Decision(False, f"{tool} is explicitly denied by policy")

        if tool in self.approval_tools:
            return Decision(
                False,
                f"{tool} requires human approval",
                requires_approval=True,
            )

        if tool in self.allowed_tools:
            return Decision(True, "allowed by policy")

        return Decision(False, f"{tool} is not present in the allowlist (deny-by-default)")
