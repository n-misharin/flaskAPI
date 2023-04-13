Пример простого web-сервера на `Python`, с использованием `flask` и `SQLite`.

## Структура

- `app/__init__.py` - файл запуска модуля.
- `database.py` - работа с БД.
- `endpoints.py` - обработчики маршрутов.
- `database.db` - база данных `SQLite`.

### Установка
`pip install -r requirements.txt`

### Запуск
`$ waitress-serve --port=80 --call app:create_app` (default IP is 0.0.0.0) Проверить можно по localhost.
