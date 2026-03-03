---
description: Backend - Добавить API-тесты на контракт endpoint-а
---

# Добавление API-тестов на контракт endpoint-а

Используй skill **backend-add-tests-api-contract** (`.cursor/skills/backend-add-tests-api-contract/SKILL.md`).

## Что сделать

Выполни workflow skill: собери тест-матрицу (success, auth/context, validation/business errors, side effects), проверь `status` + `error-code`, сверь runtime с OpenAPI-контрактом и прогони проектные тестовые команды.
