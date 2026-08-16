"""Run a few agent tool-call attempts through the policy layer."""

from audit import audit_event
from policy import PolicyEngine
from validators import validate_package_name

policy = PolicyEngine()


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
        audit_event(tool, arguments, "HITL", decision.reason)
        print(f"👤 APPROVAL REQUIRED — {decision.reason}")
        return

    if not decision.allowed:
        audit_event(tool, arguments, "BLOCKED", decision.reason)
        print(f"⛔ BLOCKED — {decision.reason}")
        return

    audit_event(tool, arguments, "ALLOWED", decision.reason)
    print(f"✓ ALLOWED — {decision.reason}")


if __name__ == "__main__":
    print("=== Secure Agent Policy Demo ===")
    attempt("read_package", {"package": "freerdp3"})
    attempt("search_cves", {"package": "freerdp3"})
    attempt("export_report", {"package": "freerdp3"})
    attempt("write_database", {"package": "freerdp3", "status": "fixed"})
    attempt("run_shell", {"command": "rm -rf /"})
    attempt("read_package", {"package": "../../etc/passwd"})
