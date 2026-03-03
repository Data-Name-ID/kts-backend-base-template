---
name: backend-add-api-endpoint-rest
description: "Backend - Создание или изменение REST API endpoint в backend-проектах стека. Использовать, когда нужно добавить новую ручку, изменить маршрут/HTTP-метод/статус-коды, подключить endpoint в роутер, настроить DI-зависимости и оформить OpenAPI-контракт для success/error ответов."
---

# Backend Add API Endpoint REST

Добавлять и дорабатывать endpoint по REST-конвенциям и локальному паттерну проекта.

## Workflow

1. Определить контракт endpoint.
- Зафиксировать ресурс, операцию, входные параметры, success-статус, список ожидаемых ошибок.
- Проверить, что operation REST-ориентирована, а не RPC под видом REST.

2. Найти локальный паттерн домена.
- Структура домена: `app/<domain>/views.py`, `schemas.py`, `accessor.py`, `models.py`, `urls.py`, `domain.py`.
- Аналог из существующего: `app/users/` (контроллер `UserController`, schemas `UserEmailRequest`, accessor `UserAccessor`).

2.1 Зафиксировать проектные паттерны.
- Endpoint тонкий: `Controller` — transport layer.
- Доступ к данным только через `store.<domain>` (Accessor). Бизнес-оркестрацию выносить в manager только при необходимости.
- `store: Store` получать через DI (регистрируется автоматически через `InitPlugin`), не инстанциировать вручную.

3. Реализовать endpoint.
- DTO request/response: `msgspec.Struct` с `kw_only=True` в `schemas.py`.
- Response оборачивать в `OkResponse` из `app.core.schemas`.
- Метод контроллера: `litestar.Controller`, декоратор `@get`/`@post`/`@patch`/`@delete` с явным `path=...` и `status_code=...`.
- Для публичных ручек добавлять `exclude_from_auth=True`.
- Валидацию входа выносить в `__post_init__` DTO, используя `app.core.validators`.

3.1 Зафиксировать версию API.
- Добавлять endpoint в текущую версию (`v1` по умолчанию, префикс `/api/...`).
- Не менять версию API самостоятельно; смену `v1` → `v2+` делать только по явному решению.

4. Зафиксировать REST-семантику.
- Коллекция: `GET /resource/` и `POST /resource/`.
- Элемент: `GET /resource/{id}/`, `PUT/PATCH /resource/{id}/`, `DELETE /resource/{id}/`.
- Статус-коды: `200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`.

5. Оформить ошибки.
- Использовать `litestar.exceptions`: `NotFoundException`, `PermissionDeniedException`, `ValidationException`, `HTTPException`.
- Бизнес-ошибки из accessor/manager маппить в HTTP-исключения Litestar в контроллере.

6. Подключить роутинг.
- Добавить контроллер в `<domain>/urls.py` в функцию `get_handlers()`.
- Зарегистрировать `get_handlers()` в `route_handlers` в `main.py`.
- Если добавляется новый accessor — добавить его в `Store` в `app/core/store.py`.

7. Проверить качество.
- `uv run ruff check .` + `uv run mypy .`.
- Добавить/обновить тесты: success + `401` + validation/business error.

## Definition Of Done

- Endpoint реализован в существующей архитектуре проекта.
- REST-метод, путь и статус-коды консистентны с контрактом.
- Контроллер подключён в `urls.py` → `main.py`, ruff/mypy проходят.
