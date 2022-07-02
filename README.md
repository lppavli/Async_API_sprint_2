## Проект Асинхронное API (5 спринт)

https://github.com/lppavli/Async_API_sprint_1
## Используемые технологии
- Код приложения пишется на Python + FastAPI.
- Приложение запускается под управлением сервера ASGI(uvicorn).
- Хранилище – ElasticSearch.
- За кеширование данных отвечает – redis cluster.
- Все компоненты системы запускаются через docker.
## Назначение и имена контейнеров в docker-compose
- postgres - база данных postgresql
- redis - redis
- etl - процесс ETL для загрузки данных из postgres в elasticsearch
- async-api - модуль FastAPI
- nginx - сервер nginx, который отдает это все во внешний мир
- tests - папка с тестами
## Для запуска проекта необходимо
- Создать в папках ETL, src, tests и в корневой папке проекта файл .env следующего содержимого:
~~~
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
DB_HOST=host
DB_PORT=port
SECRET_KEY=secret
REDIS_HOST=host
REDIS_PORT=port
ELASTIC_HOST=host
ELASTIC_PORT=port
~~~
- Собрать приложение, используя команду docker-compose build
- Запустить, используя команду docker-compose up
## Тестирование
# В контейнере
- Собрать контейнер для тестов можно командой  docker-compose -f docker-compose-test.yml up -d --build
# Локально
- перейти в папку с тестами: cd tests/functional
- установить окружение pip install -r requirements.txt
- запустить тесты pytest src
## Использование
# Документация доступна по адресу 
- http://localhost/api/openapi (в режиме тестов)
- http://localhost:8000/api/openapi (при запуске через nginx)
