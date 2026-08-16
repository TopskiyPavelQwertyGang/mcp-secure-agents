# Controls: от prompt к реальной границе безопасности

## 1. Deny by default
Если capability явно не нужна — агент её не получает.

```text
unknown tool → BLOCK
```

## 2. Allowlist
Разрешаем конкретный небольшой набор операций.

```text
read_package → allow
search_cves  → allow
run_shell    → deny
```

## 3. Least privilege
Даже разрешённый tool должен работать с минимальными правами: read-only токен, отдельная DB role, ограниченный filesystem scope.

## 4. Validation
Проверяем не только название tool, но и аргументы.

```text
read_package("freerdp3")        → OK
read_package("../../etc/passwd") → BLOCK
```

## 5. Human-in-the-Loop
Действия с side effect можно переводить в состояние `PENDING_APPROVAL` вместо автоматического выполнения.

## 6. Sandbox
Если агенту действительно нужен shell или выполнение кода, запускайте его в изолированной среде с лимитами CPU/RAM/time/network/filesystem.

## 7. Audit
Логируйте:

- кто инициировал задачу;
- какой tool выбрала модель;
- какие параметры передала;
- какое решение приняла policy;
- был ли side effect;
- кто подтвердил чувствительное действие.

## Защита слоями

```text
Prompt
  ↓
Tool exposure
  ↓
Policy / allowlist
  ↓
Input validation
  ↓
IAM / permissions
  ↓
Sandbox / HITL
  ↓
Audit
```

Ни один слой не должен быть единственной защитой.
