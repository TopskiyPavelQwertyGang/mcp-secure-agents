# Quick Start

## 1. Установить зависимости

```bash
uv sync
```

или:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" pydantic
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

## 3. Запустить MCP Inspector

```bash
uv run mcp dev server.py
```

Попробуйте вызвать:

```text
read_package(package="freerdp3")
search_cves(package="freerdp3")
```

Обратите внимание: MCP server вообще не публикует опасные write/shell tools. Это сильнее, чем публиковать опасный инструмент и надеяться, что модель его не вызовет.

## 4. Эксперимент

Откройте `policy.py` и временно добавьте новое действие в allowlist. Посмотрите, как policy меняет решение.

Главный вывод:

> Сначала ограничиваем capability технически. Prompt используем как дополнительный слой, а не как единственную защиту.
