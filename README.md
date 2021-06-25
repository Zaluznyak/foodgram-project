![foodgram workflow](https://github.com/zaluznyak/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)

Адрес сайта: http://84.252.135.106
log:admina
pas:1a2d3m4i5n
# foodgram-project

## Описание
Продуктовый помощник.

### Требования
Необходим установленный и запущенный Docker.

Инструкции по установке см. [Docker](https://www.docker.com/get-started#h_installation)

### Первый запуск проекта
     
1. Клонирование репозитория 
```bash
git clone https://github.com/Zaluznyak/infra_sp2.git
```
2. Сборка и запуск образа (находимся в корне проекта)
```bash
docker-compose up -d --build
```
3. Создание миграций
```bash
docker-compose exec web python manage.py makemigrations api
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations foodgram
```
4. Применение миграций
```bash
docker-compose exec web python manage.py migrate
```
5. Сбор статики
```bash
docker-compose exec web python manage.py collectstatic
```
6. Создание учетной записи администратора
```bash
docker-compose exec web python manage.py createsuperuser
```
7. Загрузка в базу тестовых данных
```bash
docker-compose exec web python manage.py loaddata dump.json
```
8. Переходим на сайт http://127.0.0.1

### Технологии
- Python 3.8.5
- Django 3.0.5
- DRF 3.12.4
- PostgreSQL 12.4
- nginx 1.19.3  
- Docker
