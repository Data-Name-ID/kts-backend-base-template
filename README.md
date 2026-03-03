# Название проекта

## Зависимости

- Docker Desktop [Установка](https://www.docker.com/products/docker-desktop/)

## Запуск проекта

### 1. Клонировать проект

```bash
git clone https://github.com/Data-Name-ID/kts-backend-base-template.git
```

### 2. Создать .secrets.yaml

```bash
cp example.secrets.yaml .secrets.yaml
```

Заполните файл своими данными.

### 3. Запуск

```bash
docker compose up -d --build
```

### Остановка

```bash
docker compose down
```

## Продвинутая разработка

### Локальная установка через uv

Требуется Python 3.12+ и `uv`.

Установка `uv` (macOS):

```bash
brew install uv
```

или универсальным скриптом:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Установка зависимостей проекта (включая dev-зависимости):

```bash
uv sync
```

### Локальный запуск API без Docker backend

1. Поднимите только базу данных:

    ```bash
    docker compose up -d db
    ```

2. Создайте `.secrets.yaml` и для локального запуска укажите:

    ```yaml
    db:
      host: "localhost"
      port: 5432
    ```

3. Примените миграции:

    ```bash
    uv run alembic upgrade head
    ```

4. Запустите API:

    ```bash
    uv run litestar --app main:app run -d
    ```

### Alembic: миграции

Создать миграцию (автогенерация):

```bash
uv run alembic revision --autogenerate -m "add_users_table"
```

Применить все миграции:

```bash
uv run alembic upgrade head
```

Откатить последнюю миграцию:

```bash
uv run alembic downgrade -1
```

Посмотреть текущее состояние и историю:

```bash
uv run alembic current
uv run alembic history
```

> Примечание: в `alembic.ini` включены post-write hooks (`ruff format` и `ruff check --fix`) для новых файлов миграций.

### Полезные dev-команды

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
```
