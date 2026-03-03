---
name: backend-add-crud-resource
description: "Backend - Полное добавление нового CRUD-ресурса в backend-проекте: модель, миграция, accessor, REST endpoint-ы, OpenAPI-ошибки и тесты. Использовать, когда нужно создать или расширить ресурс целиком, а не только одну ручку."
---

# Backend Add CRUD Resource

Реализовать ресурс end-to-end по существующему паттерну проекта.

## Workflow

1. Зафиксировать контракт ресурса.
- Определить имя ресурса, поля, ограничения, связи, операции CRUD.
- Определить список ошибок и правила доступа.

1.1 Зафиксировать паттерны реализации.
- Базовый поток: `Controller` → `accessor` → `model`.
- `Accessor` — единая точка работы с persistence; наследовать от `BaseAccessor`.
- `manager` — добавлять только при наличии сложной бизнес-оркестрации.
- `Store` — единый DI-реестр; новый accessor регистрировать в `app/core/store.py`.

2. Обновить слой данных.
- Создать `<domain>/models.py`: наследовать от `BaseModel`, миксины `IDMixin`, `CreatedAtMixin`, `UpdatedAtMixin`; длины строк из `StaticConfig`.
- Добавить миграцию: `uv run alembic revision --autogenerate -m "<message>"` — затем проверить upgrade/downgrade.
- Создать `<domain>/accessor.py`: методы list/create/get/update/delete; доступ через `self.store.db.<method>`.

3. Обновить бизнес-слой (если нужен).
- Добавить `<domain>/manager.py` и зарегистрировать в `Store` аналогично accessor.
- Бизнес-ошибки оформлять отдельными exception-классами; маппить в HTTP-ошибки в контроллере.

4. Добавить API-слой.
- DTO: `msgspec.Struct` с `kw_only=True` в `<domain>/schemas.py`.
- Response: `OkResponse[T]` из `app.core.schemas`.
- Endpoint-ы CRUD с REST-семантикой, `exclude_from_auth=True` для публичных ручек.
- Размещать под `/api/v1/...`; версию не повышать автоматически.
- Подключить контроллер в `<domain>/urls.py` → `get_handlers()` → `main.py`.
- Для API-части применять skill `backend-add-api-endpoint-rest`.

5. Оформить ошибки.
- Использовать `litestar.exceptions`; доменные ошибки при необходимости выносить в `<domain>/errors.py`.
- Для error-контракта применять skill `backend-http-errors-openapi`.

6. Добавить тесты.
- Минимум: list, get, create, update, delete.
- Negative: `401`, validation, not found, conflict.
- Запуск: `uv run pytest`.

7. Проверить консистентность.
- `uv run ruff check .` + `uv run mypy .`.
- Проверить, что naming, response-envelope и error-codes согласованы с проектом.

## CRUD Matrix

- `GET /resource/` -> list (`200`)
- `GET /resource/{id}/` -> detail (`200`)
- `POST /resource/` -> create (`201`)
- `PUT/PATCH /resource/{id}/` -> update (`200`)
- `DELETE /resource/{id}/` -> delete (`204`)

## Definition Of Done

- Ресурс полностью реализован от БД до API.
- CRUD-операции соответствуют REST-семантике.
- Accessor подключён в `Store`, роутинг в `main.py`.
- ruff/mypy проходят, тесты зелёные.
