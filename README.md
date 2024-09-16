# Описание проекта
Проект представляет собой API задания для стажировки в компании Авит.

## Используемые инструменты
* **Python** (3.10);
* **FastApi** (asynchronous Web Framework);
* **Docker** and **Docker Compose** (containerization);
* **PostgreSQL** (database);
* **SQLAlchemy** (working with database from Python);
* **Alembic** (database migrations made easy);
* **Pydantic** (data verification);

## Сборка и запуск приложения
1. Переименовать .env.template в .env и заполнить его
2. Собрать и запустить контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
    ```
    docker-compose up -d
    ```

## Документация

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    localhost:8080/docs/
    ```