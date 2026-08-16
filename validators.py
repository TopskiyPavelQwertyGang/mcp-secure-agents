"""Input validation for demo tool calls."""

import re

PACKAGE_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9+._-]{0,99}$")
CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)


def validate_package_name(name: str) -> str:
    if not PACKAGE_RE.fullmatch(name):
        raise ValueError("invalid package name")
    return name


def validate_cve_id(cve_id: str) -> str:
    if not CVE_RE.fullmatch(cve_id):
        raise ValueError("invalid CVE id")
    return cve_id.upper()
