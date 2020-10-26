from django import template

from recipe.models import Cart
from social.models import Favorit, Follow

register = template.Library()


@register.filter
def addclass(field, css):
    """
    Формирование тэгов для GET запроса
    """
    return field.as_widget(attrs={"class": css})


@register.filter
def rupluralize(value, endings):
    """
    Формирование названий во множественном числе
    """
    endings = endings.split(',')
    if value % 100 in (11, 12, 13, 14):
        return endings[2]
    if value % 10 == 1:
        return endings[0]
    if value % 10 in (2, 3, 4):
        return endings[1]
    else:
        return endings[2]


@register.filter
def formatting_tags(request, tag):
    """
    Формирование тэгов для GET запроса
    """
    if 'tags' in request.GET:
        tags = request.GET.get('tags')
        tags = tags.split(',')
        if tag not in tags:
            tags.append(tag)
        else:
            tags.remove(tag)
        if '' in tags:
            tags.remove('')
        result = ','.join(tags)
        return result
    return tag


@register.filter(name='recipe_in_cart')
def recipe_in_cart(recipe, user):
    """
    Проверка наличия рецепта в корзине
    """
    return Cart.objects.filter(shopper=user, recipe=recipe).exists()


@register.filter(name='in_follow')
def in_follow(author, user):
    """
    Проверка наличия автора в подписках
    """
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='in_favorite')
def in_favorite(recipe, user):
    """
    Проверка наличия рецепта в избранном
    """
    return Favorit.objects.filter(author=user, recipe=recipe).exists()
