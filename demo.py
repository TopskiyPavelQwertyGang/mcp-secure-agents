"""Run agent-like tool-call attempts through validation, policy and HITL."""

from approval import request_approval
from audit import audit_event
from policy import PolicyEngine
from validators import validate_package_name

policy = PolicyEngine()


def execute_demo_action(tool: str, arguments: dict) -> None:
    """Represent the side effect that happens only after authorization."""
    print(f"⚙ EXECUTED — {tool}({arguments})")


def attempt(tool: str, arguments: dict) -> None:
    print(f"\nAGENT → {tool}({arguments})")

    if "package" in arguments:
        try:
            validate_package_name(arguments["package"])
        except ValueError as exc:
            audit_event(tool, arguments, "BLOCKED", str(exc))
            print(f"⛔ BLOCKED — {exc}")
            return

    decision = policy.evaluate(tool, arguments)

    if decision.requires_approval:
        audit_event(tool, arguments, "HITL_REQUESTED", decision.reason)
        approval = request_approval(tool, arguments)
        if not approval.approved:
            audit_event(tool, arguments, "HITL_REJECTED", approval.reason)
            print(f"⛔ BLOCKED — {approval.reason}")
            return
        audit_event(tool, arguments, "HITL_APPROVED", approval.reason)
        execute_demo_action(tool, arguments)
        return

    if not decision.allowed:
        audit_event(tool, arguments, "BLOCKED", decision.reason)
        print(f"⛔ BLOCKED — {decision.reason}")
        return

    audit_event(tool, arguments, "ALLOWED", decision.reason)
    print(f"✓ ALLOWED — {decision.reason}")
    execute_demo_action(tool, arguments)


if __name__ == "__main__":
    print("=== Secure Agent Policy + HITL Demo ===")
    attempt("read_package", {"package": "freerdp3"})
    attempt("search_cves", {"package": "freerdp3"})
    attempt("export_report", {"package": "freerdp3"})
    attempt("write_database", {"package": "freerdp3", "status": "fixed"})
    attempt("run_shell", {"command": "rm -rf /"})
    attempt("read_package", {"package": "../../etc/passwd"})
