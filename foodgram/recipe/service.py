from recipe.models import Tag


def get_ingredients_from_js(request):
    """
    Получение ингредиентов из формы рецепта,
    для дальнейшего сохранения в БД
    """
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(
                request.POST[f'valueIngredient_{_[1]}']
            )
    return ingredients


def get_tags_from_get(request):
    """
    Фильтрация для тэгов из GET запроса
    """
    tags_from_get = []
    if 'tags' in request.GET:
        tags_from_get = request.GET.get('tags')
        _ = tags_from_get.split(',')
        tags_qs = Tag.objects.filter(title__in=_).values('title')
    else:
        tags_qs = False
    return [tags_qs, tags_from_get]
