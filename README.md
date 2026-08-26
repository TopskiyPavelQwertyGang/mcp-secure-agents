# MCP Secure Agents

Практический репозиторий про **безопасных AI-агентов**: минимальные права, allowlist, валидация, Human-in-the-Loop, sandbox и аудит.

> Главная идея: **модель может ошибаться — система не обязана позволять ей выполнить опасное действие.**

## Базовая схема

```text
USER → AGENT → POLICY → TOOL → RESULT
                    ↓
                  BLOCK
```

Агент выбирает действие, но выполнение контролируется отдельным слоем политик.

**Prompt ≠ Security Boundary.**

## Что здесь есть

- минимальные права;
- allowlist инструментов;
- валидация параметров;
- блокировка опасных операций;
- Human-in-the-Loop для чувствительных действий;
- журналирование решений;
- простой policy engine.

## Демо-сценарий

Пользователь ставит задачу анализа пакета. Агент может читать разрешённые данные и искать сведения об уязвимостях, но изменение данных и произвольные shell-команды запрещены политикой.

```text
READ DATA       → ALLOWED
SEARCH DATA     → ALLOWED
EXPORT RESULT   → approval / policy
WRITE DATA      → BLOCKED
RUN SHELL       → BLOCKED
```

Это демонстрирует принцип из доклада: **границы задаются архитектурой и политиками, а не обещанием модели вести себя безопасно.**

## Security controls

### Allowlist
Агент видит только явно разрешённые инструменты.

### Least privilege
Каждый инструмент получает минимально необходимые права.

### Validation
Параметры tool-call проверяются до выполнения.

### Human-in-the-Loop
Чувствительное действие можно остановить до исполнения и передать решение человеку.

### Sandbox
Код и потенциально опасные операции выполняются в изолированной среде.

### Audit
Решения, разрешения и блокировки фиксируются для последующего анализа.

## Быстрый старт

### Требования

- Python 3.10+
- `uv` или `pip`

```bash
git clone https://github.com/TopskiyPavelQwertyGang/mcp-secure-agents.git
cd mcp-secure-agents
uv sync
uv run python demo.py
```

MCP server:

```bash
uv run mcp dev server.py
```

## Что попробовать руками

1. Запустить `demo.py`.
2. Посмотреть разрешённые действия.
3. Попробовать запрещённое действие и увидеть `BLOCKED`.
4. Изменить `policies/agent-policy.yaml`.
5. Запустить пример повторно и увидеть, как политика меняет поведение системы.

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
└── docs/
    ├── threat-model.md
    └── controls.md
```

## Learning path

1. **mcp-protocol-guide** — понять MCP.
2. **mcp-secure-agents** — понять границы и policy enforcement.
3. **mcp-use-cases** — применить подход к своим сценариям.

## Важно

Это **учебный security lab**, а не production-ready security framework. Примеры намеренно абстрактны и не описывают внутреннюю архитектуру, политики или процессы какой-либо организации.

Для production потребуются собственная модель угроз, IAM, управление секретами, наблюдаемость, rate limits, аудит и другие контроли в зависимости от сценария.

---

**Prompt ≠ Security Boundary**