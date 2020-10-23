from django.db import models
from django.contrib.auth import get_user_model
from recipe.models import Recipe

User = get_user_model()


class Favorit(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_favorit"
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_favorit"
        )

    def __str__(self):
        return f'author - {self.author} | recipe - {self.recipe.title}'

    class Meta:
        unique_together = ('author', 'recipe')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
        )

    def __str__(self):
        return f'follower - {self.user} | following - {self.author}'

    class Meta:
        unique_together = ('user', 'author')


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments"
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_authors"
        )
    text = models.TextField(blank=False, null=False)
    created = models.DateTimeField("comment_date_pub", auto_now_add=True)

    def __str__(self):
        return self.text
