import datetime as dt

from django.shortcuts import render
from recipe.models import Cart


def cart_list_counter(request):
    """
    Счётчик рецептов в корзине
    """
    if request.user.is_authenticated:
        count = request.user.shoppers.all().count()
    else:
        count = []
    return {'count': count}


def year(request):
    """
    Добавляет переменную с текущим годом
    """
    current_year = dt.datetime.today().year
    return {'year': current_year}


def paginator_page(request):
    """
    Вставка номера страницы в кнопку пагинатора
    """
    result_str = ''
    for item in request.GET.getlist('pages'):
        result_str += f'&pages={item}'
    return {'pages': result_str}
