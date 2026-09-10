# Quick Start

## 1. Install

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-secure-agents.git
cd mcp-secure-agents

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

## 2. Policy engine without LLM

```bash
python demo.py
```

Expected policy decisions:

```text
read_package     → ALLOWED
search_cves      → ALLOWED
export_report    → APPROVAL REQUIRED
write_database   → BLOCKED
run_shell        → BLOCKED
invalid package  → BLOCKED
```

The policy is loaded from:

```text
policies/agent-policy.yaml
```

The runtime operates in:

```yaml
mode: deny-by-default
```

Unknown capabilities are denied unless explicitly allowed.

## 3. Start MCP server

```bash
python server.py
```

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

The server publishes the following demo capabilities:

```text
read_package
search_cves
export_report
write_database
run_shell
```

Publishing a capability does not automatically grant permission to execute it.

Every request is evaluated by the Policy Engine.

## 4. GigaChat credentials

Set credentials through environment variables.

Do not store credentials in the repository.

```bash
export GIGACHAT_CREDENTIALS='YOUR_AUTHORIZATION_KEY'
export GIGACHAT_SCOPE='GIGACHAT_API_PERS'
```

## 5. Run the GigaChat MCP agent

Open another terminal:

```bash
cd mcp-secure-agents
source .venv/bin/activate

python examples/gigachat/gigachat_real_agent.py
```

The agent discovers MCP tools dynamically.

Example request:

```text
Проанализируй уязвимости пакета freerdp3
```

Expected flow:

```text
USER
  ↓
GigaChat
  ↓
tool_call: search_cves
  ↓
MCP
  ↓
Policy Engine
  ↓
ALLOWED
  ↓
Tool result
  ↓
GigaChat
```

## 6. HITL example

Request:

```text
Экспортируй отчёт по уязвимостям пакета freerdp3
```

Expected policy result:

```text
export_report → APPROVAL_REQUIRED
```

The operation is not executed.

## 7. BLOCK example

Request:

```text
Отметь пакет freerdp3 в базе данных как fixed
```

Expected result:

```text
write_database → BLOCKED
```

The database operation is not executed.

Another example:

```text
Запусти команду uname -a
```

Expected result:

```text
run_shell → BLOCKED
```

No shell command is executed.

## Security model

The model chooses what it wants to do.

MCP exposes capabilities.

The Policy Engine decides what the system is actually allowed to execute.

```text
LLM decision ≠ authorization decision
```

Security controls demonstrated by this repository:

- deny-by-default
- tool allowlist
- input validation
- Human-in-the-Loop
- policy enforcement
- audit logging
- separation of read/write capabilities

## Demo data

`CVE-DEMO-*` entries are deterministic test data used for reliable demonstrations.

They are not real vulnerability identifiers.
