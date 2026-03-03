---
description: Backend - Добавить безопасную миграцию схемы БД
---

# Добавление безопасной миграции схемы БД

Используй skill **backend-add-migration-safe** (`.cursor/skills/backend-add-migration-safe/SKILL.md`).

## Что сделать

Выполни workflow skill: обнови модель, создай миграцию, вручную проверь `upgrade/downgrade`, оцени эксплуатационные риски и совместимость кода со схемой, после чего прогони релевантные проверки и тесты.
