# Foodgram

![workflow status](https://github.com/YanaYugai/foodgram-project-react_fast_api/actions/workflows/main.yml/badge.svg)

## Описание проекта

Foodgram позволяет пользователям создавать свои рецепты, подписываться на других авторов и многое другое. Проект был создан в рамках самообучения для освоения FastApi, SqlAlchemy, Alembic, Pytest.

## Технологии

* FastApi
* Nginx
* Docker
* SQLAlchemy
* PostgreSQL
* pre-commit

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:YanaYugai/foodgram-project-react_fast_api.git
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Прописать все необходимые переменные в .env:

Переменные, которые вам понадобятся:
1. POSTGRES_USER
2. POSTGRES_PASSWORD
3. POSTGRES_DB
4. DB_HOST
5. DB_PORT
6. DB_NAME
7. DB_USER
8. DB_PASS
9. MINUTES
10. SECRET_KEY

Запустить локально docker compose:

```bash
docker compose up -d
```

## Документация:

После запуска проекта вам будет доступна его документаци по адресу: http://127.0.0.1:8000/api/docs/

## Автор

YanaYugai(https://github.com/YanaYugai)
