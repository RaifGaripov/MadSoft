# Коллекция мемов

## Описание

Этот проект представляет собой веб-приложение, созданное с использованием FastAPI, которое предоставляет API для управления коллекцией мемов. Приложение состоит из двух основных сервисов: общедоступного API для бизнес-логики и медиа-сервиса для обработки медиа-файлов с использованием S3-совместимого хранилища (MinIO).

## API

- **GET /memes**: Получить список всех мемов (с нумерацией страниц).
- **GET /memes/{id}**: Получить конкретный мем по его id.
- **POST /memes**: Добавить новый мем (с изображением и текстом).
- **PUT /memes/{id}**: Обновите существующий мем по id.
- **DELETE /memes/{id}**: Удалить мем по id.

## Требования

- [Docker](https://www.docker.com/) and Docker Compose

## Установка и запуск

1. Склонировать репозиторий:

```bash
git clone https://github.com/yourusername/meme_app.git
cd meme_app
```
2. Установить [Docker](https://www.docker.com/)
3. Из папки проекта выполнить docker-compose файл
```bash
docker-compose up --build
```
Для проверки API открытого [http://localhost:80/docs](http://localhost:80/docs)

Закрытое API [http://localhost:8000/docs](http://localhost:8000/docs)

UI для хранилища MinIO [http://localhost:9090](http://localhost:9090)

Логин: minioadmin

Пароль: minioadmin 

Для запуска тестов
```bash
docker exec -it madsoft-public_api-1 pytest
```