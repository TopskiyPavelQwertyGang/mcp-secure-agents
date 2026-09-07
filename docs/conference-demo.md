# Conference demo: security enforcement

This scenario complements the CVE analysis use case by showing what happens when an agent requests capabilities with different risk levels.

```text
AGENT TOOL REQUEST
       ↓
INPUT VALIDATION
       ↓
POLICY ENGINE
   ┌───┼────────────┐
   ↓   ↓            ↓
ALLOW  HITL         DENY
   ↓   ↓            ↓
EXEC  HUMAN       BLOCK + AUDIT
```

## Demo sequence

Run:

```bash
uv run python demo.py
```

The script demonstrates:

- `read_package` → allowed and executed;
- `search_cves` → allowed and executed;
- `export_report` → pauses at a real CLI approval gate, then executes only after approval;
- `write_database` → denied by policy;
- `run_shell` → denied by policy;
- `../../etc/passwd` as a package name → rejected by input validation before tool execution.

## Speaker message

The important part is not whether the model can be instructed to behave. The important part is that the execution path does not trust the model's decision. Authorization happens after the model chooses an action and before the side effect.

## Scope

The CLI approval gate is deliberately small and synchronous so the control is visible during a talk. Production HITL would normally use authenticated identities, durable approval state, expiry, separation of duties and a tamper-resistant audit trail.
