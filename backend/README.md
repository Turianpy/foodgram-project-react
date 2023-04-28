# Workflow status ![badge](https://github.com/Turianpy/api_foodgram/workflows/foodgram_workflow/badge.svg)

# Описание проекта Foodgram

Foodgram - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий
- Django-gunicorn
- PostgreSQL
- Nginx
- Docker

## Установка
1. Клонируйте репозиторий с проектом

2. Перейдите в папку infra

3. В папке infra создайте файл .env и заполните его своими значениями переменных окружения:
```shell
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных>
POSTGRES_USER=<имя пользователя>
POSTGRES_PASSWORD=<пароль>
DB_HOST=<адрес хоста или название контейнера (db по умолчанию)>
DB_PORT=5432
```

4. Запустите docker-compose:
```shell
docker-compose up -d --build
```

5. Выполните миграции:
```shell
docker-compose exec -i infra_backend_1 python manage.py makemigrations
docker-compose exec -i infra_backend_1 python manage.py migrate --noinput
```

6. (не обязательно) Соберите статику:
```shell
docker-compose exec -i infra_backend_1 python manage.py collectstatic --no-input
```

Сайт будет доступен на localhost, а API на localhost/api

## Доступ к запущенному проекту в Yandex Cloud

Сайт доступен по адресу http://158.160.62.222

API доступно по адресу http://158.160.62.222/api