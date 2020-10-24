from django.db import models
from django.contrib.auth import get_user_model
from recipe.models import Recipe

User = get_user_model()


class Favorit(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorits',
        verbose_name='Автор'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorits',
        verbose_name='Избранное'
        )

    def __str__(self):
        return f'author - {self.author} | recipe - {self.recipe.title}'

    class Meta:
        unique_together = ('author', 'recipe')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
        )

    def __str__(self):
        return f'follower - {self.user} | following - {self.author}'

    class Meta:
        unique_together = ('user', 'author')


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарии'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_authors',
        verbose_name='Авторы комментариев'
        )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст'
        )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
        )

    def __str__(self):
        return self.text
