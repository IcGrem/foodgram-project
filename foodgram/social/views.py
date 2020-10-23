import json

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .forms import CommentForm
from recipe.models import Recipe, Tag, User
from social.models import Comment, Follow, Favorit


@login_required
def follow_index(request):
    """
    Страница подписок на профили авторов рецептов
    """
    follows = Follow.objects.select_related(
        'user', 'author'
        ).filter(user=request.user)
    paginator = Paginator(follows, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator,
        })


class Following(View):
    """
    Добавление профиля автора в подписки
    и удаление профиля из подписок
    """
    def post(self, request):
        author_id = json.loads(request.body)['id']
        author = get_object_or_404(User, id=author_id)
        Follow.objects.get_or_create(
            user=request.user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        user = get_object_or_404(User, username=request.user.username)
        author = get_object_or_404(User, id=author_id)
        following = get_object_or_404(Follow, user=user, author=author)
        following.delete()
        return JsonResponse({'success': True})


@login_required
def favorit_index(request):
    """
    Страница избранных рецептов
    """
    favorit_recipe_list = Recipe.objects.select_related(
        'author'
        ).prefetch_related('tags',).filter(recipe_favorit__author=request.user)
    tags_list = []
    if 'tags' in request.GET:
        tags_list = request.GET.get('tags')
        _ = tags_list.split(',')
        tags_qs = Tag.objects.filter(title__in=_).values('title')
        if tags_qs:
            favorit_recipe_list = Recipe.objects.filter(
                recipe_favorit__author=request.user, tags__title__in=tags_qs
            ).distinct()
    paginator = Paginator(favorit_recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorit.html', {
        'page': page,
        'paginator': paginator,
        'recipe': favorit_recipe_list,
        'tags': tags_list
    })


class Favorites(View):
    """
    Добавление рецепта в избранные и удаление из него
    """
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorit.objects.get_or_create(author=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        author = get_object_or_404(User, username=request.user.username)
        favorit = get_object_or_404(Favorit, author=author, recipe=recipe)
        favorit.delete()
        return JsonResponse({'success': True})


@login_required
def add_comment(request, recipe_id):
    """
    Добавление комментария
    """
    user = get_object_or_404(User, username=request.user)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = CommentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = user
            comment.save()
            return redirect('recipe', recipe_id)
    else:
        form = CommentForm()
    return render(request, 'recipe.html', {
        'username': username,
        'recipe_id': recipe_id,
        'recipe': recipe,
        'form': form
        })
