![foodgram-workflow](https://github.com/IcGrem/foodgram-project/workflows/foodgram-workflow/badge.svg)


# Проект: Foodgram [«Продуктовый помощник»](http://food-gram.ga/)  
### Это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», комментировать рецепты других авторов, а перед походом в магазин скачивать в формате pdf сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.  

## Технологий стэк
- Python
- Django
- PostgreSQL
- Gunicorn
- Nginx
- Docker
- GitHub actions  

Проект выполнен в качестве дипломного задания курса Python-разработчик Яндекс.Практикум.  

## Установка на локальный компьютер
Для установки на локальном компьютере необходимо:
1. Установить Docker
2. Скачать файлы проекта из репозитория или клонировать его:
```https://github.com/IcGrem/foodgram-project.git```
3. В директории проекта `<project_name>/foodgram/` необходимо создать файл .env, в котором указать переменные окружения (например):
- DB_NAME=postgres
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
- SECRET_KEY=можно сгенерировать [по адресу](https://djecrety.ir)

4. Для сборки и запуска контейнеров необходимо перейти в папку `<project_name>/foodgram/` и выполните команду:  
    ```docker-compose up -d --build```

В результате установки будут запущены три контейнера: первый - приложение foodgram + gunicorn, второй - база данных PostgreSQL, третий - веб-сервер NGINX, настроенный на адрес http://localhost  

Зависимости, миграции и данные, необходимые для работы сервиса (список ингредиентов) будут установлены автоматически.  
Для создания в системе __суперпользователя__ выполните команду:  
    ```docker-compose exec web python manage.py createsuperuser```

Пример работы сервиса можно посмотреть на http://food-gram.ga/
