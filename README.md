# MCP Secure Agents

Практический репозиторий про **безопасных AI-агентов**: минимальные права, allowlist, валидация, Human-in-the-Loop и sandbox.

> Цель: показать, что модель может ошибаться — но система не обязана позволять ей выполнить опасное действие.

## Что здесь есть

- защищённый MCP-agent для анализа уязвимостей;
- read-only доступ к данным;
- allowlist разрешённых инструментов;
- блокировка WRITE / DELETE / shell-команд;
- валидация входных параметров;
- Human-in-the-Loop для чувствительных действий;
- журналирование решений и блокировок;
- простой policy engine, который легко расширять.

## Главная идея

```text
USER → AGENT → POLICY → TOOL → RESULT
                    ↓
                 BLOCK
```

Агент может решить, что ему нужен инструмент. Но перед выполнением запрос проходит через политику безопасности.

## Демо-сценарий

Пользователь просит:

```text
Проверь уязвимости пакета freerdp3
```

Агенту разрешено:

```text
READ package info
READ CVE database
CALL allowed API
```

Если агент попробует сделать:

```sql
UPDATE vulnerabilities SET status='fixed';
```

он получит:

```text
BLOCKED
reason: write_database is not allowed
```

Это и есть главный security boundary: не просьба в system prompt, а технически enforced policy.

## Быстрый старт

### Требования

- Python 3.10+
- `uv` или `pip`

### Установка

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-secure-agents.git
cd mcp-secure-agents
uv sync
```

Или:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" pydantic
```

### Запуск демо policy engine

```bash
uv run python demo.py
```

### Запуск MCP server

```bash
uv run mcp dev server.py
```

## Структура

```text
.
├── README.md
├── QUICKSTART.md
├── demo.py
├── server.py
├── policy.py
├── validators.py
├── audit.py
├── pyproject.toml
├── policies/
│   └── agent-policy.yaml
├── examples/
│   ├── allowed.json
│   └── blocked.json
└── docs/
    ├── threat-model.md
    └── controls.md
```

## Security controls

### 1. Allowlist
Только явно разрешённые инструменты доступны агенту.

### 2. Permissions
Каждый инструмент получает минимально необходимые права.

### 3. Validation
Параметры tool-call проходят проверку до выполнения.

### 4. HITL
Чувствительные операции требуют подтверждения человека.

### 5. Sandbox
Опасные действия должны выполняться в изолированной среде.

## Что попробовать руками

1. Запустите `demo.py`.
2. Посмотрите разрешённые действия.
3. Попробуйте `write_database` — получите блокировку.
4. Измените `policies/agent-policy.yaml`.
5. Повторите запуск и посмотрите, как меняется поведение агента.

## Learning path

1. **mcp-protocol-guide** — понять MCP.
2. **mcp-secure-agents** — научиться безопасно давать агентам инструменты.
3. **mcp-use-cases** — перейти к рабочим сценариям.

## Важно

Этот проект — учебный security lab. Не используйте demo-policy как готовую production-защиту без адаптации под вашу инфраструктуру, модель угроз, IAM и процессы аудита.

---

**Prompt ≠ Security Boundary**

Безопасность должна обеспечиваться не обещанием модели, а архитектурой системы.