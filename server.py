"""Educational MCP server exposing only low-risk read operations."""

from mcp.server.fastmcp import FastMCP

from audit import audit_event
from policy import PolicyEngine
from validators import validate_package_name

mcp = FastMCP("Secure Vulnerability Agent")
policy = PolicyEngine()

DEMO_CVES = {
    "freerdp3": [
        {"id": "CVE-DEMO-0001", "severity": "HIGH", "status": "open"},
        {"id": "CVE-DEMO-0002", "severity": "MEDIUM", "status": "review"},
    ],
    "curl": [{"id": "CVE-DEMO-0003", "severity": "LOW", "status": "review"}],
}


def authorize(tool: str, arguments: dict) -> None:
    decision = policy.evaluate(tool, arguments)
    if not decision.allowed:
        audit_event(tool, arguments, "BLOCKED", decision.reason)
        raise PermissionError(decision.reason)
    audit_event(tool, arguments, "ALLOWED", decision.reason)


@mcp.tool()
def read_package(package: str) -> dict:
    """Read demo package metadata. This tool has no write capability."""
    package = validate_package_name(package)
    args = {"package": package}
    authorize("read_package", args)
    return {"package": package, "source": "demo", "write_access": False}


@mcp.tool()
def search_cves(package: str) -> list[dict]:
    """Search a local demo CVE dataset for a package."""
    package = validate_package_name(package)
    args = {"package": package}
    authorize("search_cves", args)
    return DEMO_CVES.get(package.lower(), [])


@mcp.resource("policy://summary")
def policy_summary() -> str:
    return "Allowed: read_package, search_cves, get_report. Writes and shell execution are denied."


@mcp.prompt()
def secure_analysis(package: str) -> str:
    return (
        f"Проанализируй пакет {package}. Используй только доступные read-only инструменты. "
        "Не пытайся изменять данные. Если для продолжения требуется изменение состояния, "
        "остановись и запроси подтверждение человека."
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
