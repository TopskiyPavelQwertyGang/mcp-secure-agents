"""Secure MCP server for the AI vulnerability-agent demo."""

from mcp.server.fastmcp import FastMCP

from audit import audit_event
from policy import PolicyEngine
from validators import validate_package_name


mcp = FastMCP("Secure Vulnerability Agent")
policy = PolicyEngine()


DEMO_CVES = {
    "freerdp3": [
        {
            "id": "CVE-DEMO-0001",
            "severity": "HIGH",
            "status": "open",
        },
        {
            "id": "CVE-DEMO-0002",
            "severity": "MEDIUM",
            "status": "review",
        },
    ],
    "curl": [
        {
            "id": "CVE-DEMO-0003",
            "severity": "LOW",
            "status": "review",
        }
    ],
}


def policy_decision(tool: str, arguments: dict) -> dict:
    decision = policy.evaluate(tool, arguments)

    if decision.requires_approval:
        audit_event(
            tool,
            arguments,
            "HITL",
            decision.reason,
        )

        return {
            "status": "APPROVAL_REQUIRED",
            "tool": tool,
            "reason": decision.reason,
            "executed": False,
        }

    if not decision.allowed:
        audit_event(
            tool,
            arguments,
            "BLOCKED",
            decision.reason,
        )

        return {
            "status": "BLOCKED",
            "tool": tool,
            "reason": decision.reason,
            "executed": False,
        }

    audit_event(
        tool,
        arguments,
        "ALLOWED",
        decision.reason,
    )

    return {
        "status": "ALLOWED",
        "tool": tool,
        "reason": decision.reason,
        "executed": True,
    }


@mcp.tool()
def read_package(package: str) -> dict:
    """Read package metadata without modifying system state."""

    package = validate_package_name(package)
    args = {"package": package}

    decision = policy_decision("read_package", args)

    if decision["status"] != "ALLOWED":
        return decision

    return {
        "status": "ALLOWED",
        "package": package,
        "source": "demo",
        "write_access": False,
    }


@mcp.tool()
def search_cves(package: str) -> dict:
    """Search vulnerability information for a package."""

    package = validate_package_name(package)
    args = {"package": package}

    decision = policy_decision("search_cves", args)

    if decision["status"] != "ALLOWED":
        return decision

    return {
        "status": "ALLOWED",
        "package": package,
        "vulnerabilities": DEMO_CVES.get(package.lower(), []),
    }


@mcp.tool()
def export_report(package: str) -> dict:
    """Export a vulnerability report. This action may require human approval."""

    package = validate_package_name(package)
    args = {"package": package}

    return policy_decision("export_report", args)


@mcp.tool()
def write_database(package: str, status: str) -> dict:
    """Update vulnerability status in the database."""

    package = validate_package_name(package)

    args = {
        "package": package,
        "status": status,
    }

    return policy_decision("write_database", args)


@mcp.tool()
def run_shell(command: str) -> dict:
    """Request execution of an operating-system command."""

    args = {"command": command}

    return policy_decision("run_shell", args)


@mcp.resource("policy://summary")
def policy_summary() -> str:
    return (
        "read_package/search_cves: allowed; "
        "export_report: human approval; "
        "write_database/run_shell: denied."
    )


@mcp.prompt()
def secure_analysis(package: str) -> str:
    return (
        f"Проанализируй пакет {package}. "
        "Используй доступные MCP-инструменты. "
        "Любое действие проходит через Policy Engine. "
        "Если политика требует подтверждения человека или блокирует действие, "
        "не пытайся обходить ограничение."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
