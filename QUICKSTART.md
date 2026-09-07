# Quick Start

## 1. Установить зависимости

```bash
uv sync
```

или:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" pydantic PyYAML
```

## 2. Увидеть policy engine без LLM

```bash
python demo.py
```

Ожидаемая логика:

```text
read_package     → ALLOWED
search_cves      → ALLOWED
export_report    → APPROVAL REQUIRED
write_database   → BLOCKED
run_shell        → BLOCKED
invalid package  → BLOCKED
```

Политика загружается из `policies/agent-policy.yaml`. `PolicyEngine` не хранит отдельный hard-coded allowlist: YAML является источником правил для runtime-решений.

Ключевой режим:

```yaml
mode: deny-by-default
```

Неизвестный tool автоматически блокируется, если он явно не разрешён.

## 3. Проверить policy-as-code

Измените `policies/agent-policy.yaml`, например временно перенесите `export_report` из `human_approval` в `allowed_tools`, и повторно запустите:

```bash
python demo.py
```

Решение должно измениться без правок `policy.py`.

## 4. Запустить MCP Inspector

```bash
uv run mcp dev server.py
```

Попробуйте вызвать:

```text
read_package(package="freerdp3")
search_cves(package="freerdp3")
```

Обратите внимание: MCP server вообще не публикует опасные write/shell tools. Это сильнее, чем публиковать опасный инструмент и надеяться, что модель его не вызовет.

## 5. Security layers

В демо отдельно проверяются:

- capability policy: ALLOW / HITL / BLOCK;
- deny-by-default;
- input validation;
- audit trail;
- separation read/write capabilities.

Главный вывод:

> Агент может предложить действие, но право выполнить его определяется политикой системы, а не моделью.
