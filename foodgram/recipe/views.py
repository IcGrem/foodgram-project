import json

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa

from recipe.forms import RecipeForm
from recipe.models import (
    Cart, Ingredient, Recipe, RecipeIngredient, Tag, User)
from recipe.service import get_ingredients_from_js, get_tags_from_get
from social.forms import CommentForm
from social.models import Comment


def page_not_found(request, exception):
    """
    Cтраница 404
    """
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    """
    Cтраница 500
    """
    return render(request, 'misc/500.html', status=500)


def index(request):
    """
    Главная страница
    """
    recipes = Recipe.objects.select_related(
        'author').prefetch_related('tags',)
    #  https://otus.ru/nest/post/286/
    tags_qs, tags_from_get = get_tags_from_get(request)
    if tags_qs:
        recipes = Recipe.objects.filter(
                tags__title__in=tags_qs).distinct()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'recipe': recipes,
        'tags': tags_from_get
        })


def profile(request, username):
    """
    Страница пользователя
    """
    profile = get_object_or_404(User, username=username)
    profile_recipes = profile.author_recipes.all()
    tags_qs, tags_from_get = get_tags_from_get(request)
    if tags_qs:
        profile_recipes = Recipe.objects.filter(
            author=profile, tags__title__in=tags_qs).distinct()
    paginator = Paginator(profile_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'profile': profile,
        'recipe': profile_recipes,
        'tags': tags_from_get
        })


def recipe_view(request, recipe_id):
    """
    Просмотр рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()
    form = CommentForm()

    return render(request, 'includes/recipe.html', {
        'recipe': recipe,
        'form': form,
        'comments': comments,
        })


@login_required
def recipe_new(request):
    """
    Создание рецепта
    """
    author = get_object_or_404(User, username=request.user)
    recipe_form = RecipeForm(
        request.POST or None, files=request.FILES or None
        )
    ingredients = get_ingredients_from_js(request)
    if recipe_form.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.author = author
        recipe.save()
        for title, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            recipe_ingredient = RecipeIngredient(
                quantity=quantity,
                ingredient=ingredient,
                recipe=recipe
                )
            recipe_ingredient.save()
        recipe_form.save_m2m()
        return redirect('index')
    return render(request, 'recipe_form.html', {'form': recipe_form, })


@login_required
def recipe_edit(request, recipe_id):
    """
    Редактирование рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe.id)
    recipe_form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe)
    ingredients = get_ingredients_from_js(request)
    if recipe_form.is_valid():
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        recipe.recipe_quantities.all().delete()
        for title, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            recipe_ingredient = RecipeIngredient(
                quantity=quantity,
                ingredient=ingredient,
                recipe=recipe
                )
            recipe_ingredient.save()
        recipe_form.save_m2m()
        return redirect('index')
    return render(request, 'recipe_change_form.html', {
        'form': recipe_form,
        'recipe': recipe,
        })


@login_required
def recipe_delete(request, recipe_id):
    """
    Удаление рецепта.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


class Ingredients(View):
    """
    Фильтрация ингредиентов по GET запросу от js
    """
    def get(self, request):
        ingredient = request.GET['query']
        ingredients = list(Ingredient.objects.filter(
            title__icontains=ingredient).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)


class Purchases(View):
    """
    Добавление рецепта в корзину и удаление из неё
    """
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.get_or_create(
            shopper=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = get_object_or_404(User, username=request.user.username)
        obj = get_object_or_404(Cart, shopper=user, recipe=recipe)
        obj.delete()
        return JsonResponse({'success': True})


@login_required
def cart_list(request):
    """
    Список рецептов в корзине
    """
    recipes = request.user.shoppers.all()
    return render(request, 'cart_list.html', {'recipes': recipes})


@login_required
def cart_delete_recipe(request, recipe_id):
    """
    Удаление рецепта из корзины
    """
    recipe = get_object_or_404(Cart, shopper=request.user, recipe=recipe_id)
    recipe.delete()
    return redirect('cart_list')


@login_required
def cart_list_download(request):
    """
    Формирование и скачивание списка ингредиентов в PDF
    """
    recipes = Recipe.objects.filter(cart_recipes__shopper=request.user).values(
        'ingredients__title', 'ingredients__dimension',)
    ingredients = recipes.annotate(
        Sum('recipe_quantities__quantity')).order_by()
    template_path = 'cart_to_pdf.html'
    context = {'ingredients': ingredients}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shop_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
