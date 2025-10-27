# 🧾 AITI Guru — Тестовое задание

Сервис на **FastAPI** для управления клиентами, категориями, товарами и заказами.  
Проект реализует реляционную схему PostgreSQL с поддержкой **иерархических категорий любой глубины**, учётом остатков на складе и REST API для добавления товаров в заказ.

---

## 🚀 Основные возможности

- Реляционная схема базы данных (PostgreSQL):
  - Клиенты  
  - Категории товаров (дерево категорий через closure table, наполнение с помощью триггера)
  - Товары  
  - Заказы и позиции заказов  
  - Статусы заказов и история их изменений (история изменений автоматическая через триггер)
- REST API для работы с заказами:
  - Добавление товара в заказ (`POST /v1/orders/{order_id}/product`)
  - Если товар уже в заказе — количество увеличивается
  - Проверка остатков на складе и ошибок при нехватке
- Аналитические SQL-запросы:
  - Топ-5 самых продаваемых товаров за последний месяц  
- Асинхронное подключение к PostgreSQL через **asyncpg**
- Транзакционное выполнение операций с помощью **Dishka**
- Настроено форматирование и линтинг (**Black**, **isort**, **Ruff**)
- Готово к запуску в Docker

---

## 🧩 Технологии

| Компонент | Технология |
|------------|-------------|
| Язык | Python 3.13+ |
| Веб-фреймворк | FastAPI |
| База данных | PostgreSQL |
| Работа с БД | asyncpg |
| DI-контейнер | Dishka |
| Конфигурация | pydantic-settings |
| Миграции | yoyo-migrations |
| Линтеры и стиль | Ruff, Black, isort |
| Контейнеризация | Docker Compose |

---

## 📁 Структура проекта
```
app
   |-- api
   |   |-- __main__.py
   |   |-- v1
   |   |   |-- __init__.py
   |   |   |-- views
   |   |   |   |-- orders
   |   |   |   |   |-- views.py
   |-- config.py
   |-- migrations.py
   |-- migrations
   |   |-- 0001.initial.sql
   |   |-- 0002.change_status_trigger.sql
   |   |-- 0003.category_closure_trigger.sql
   |   |-- 0004.top5last30days.sql
   |   |-- 0005.populate_tables.sql
   |-- repository
   |   |-- exceptions.py
   |   |-- helpers.py
   |   |-- models.py
   |   |-- orders
   |   |   |-- __init__.py
   |   |   |-- exceptions.py
   |   |   |-- models.py
   |   |   |-- repository.py
   |   |-- provider.py
   |   |-- repository.py
   |   |-- repository_controller.py
deployments
   |-- .env
   |-- app
   |   |-- Dockerfile
   |-- docker-compose.dev.yml
pyproject.toml
uv.lock
```
# Запуск
`make dev-run` - создать нужные контейнеры и запустить проект, затем зайти на `localhost:8080/docs`