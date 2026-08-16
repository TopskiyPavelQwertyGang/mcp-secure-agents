"""Very small audit logger for the learning demo."""

import json
from datetime import datetime, timezone
from typing import Any


def audit_event(tool: str, arguments: dict[str, Any], status: str, reason: str) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "arguments": arguments,
        "status": status,
        "reason": reason,
    }
    print("AUDIT", json.dumps(event, ensure_ascii=False))
