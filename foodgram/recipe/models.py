from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    tag_options = {
        'breakfast': ['orange', 'Завтрак'],
        'lunch': ['green', 'Обед'],
        'dinner': ['purple', 'Ужин']
        }

    TAG_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ]
    title = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        verbose_name='Название тэга'
        )

    def __str__(self):
        return self.title

    @property
    def color(self):
        return self.tag_options[self.title][0]

    @property
    def name(self):
        return self.tag_options[self.title][1]


class Ingredient(models.Model):

    title = models.CharField(
        max_length=300,
        verbose_name='Название'
        )
    dimension = models.CharField(
        max_length=20,
        verbose_name='Единица измерения')

    def __str__(self):
        return str(self.title)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
        )
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='ingredients',
        verbose_name='Ингредиенты'
        )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
        )
    tag = models.ManyToManyField(
        Tag, related_name='tags',
        verbose_name='Тэги'
        )
    image = models.ImageField(
        upload_to='recipe/',
        default='default/default_img.jpg',
        verbose_name='Изображение'
        )

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-pub_date']

    def get_ingredients(self):
        return '\n'.join(
            self.ingredient.all().values_list('title', flat=True))
    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self):
        return '\n'.join(
            self.tag.all().values_list('title', flat=True))
    get_tags.short_description = 'Тэги'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantities',
        verbose_name='Рецепт'
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
        )
    quantity = models.FloatField(verbose_name='Количество')

    def __str__(self):
        return str(self.ingredient)


class Cart(models.Model):
    shopper = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Покупатель'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_carts',
        verbose_name='Список рецептов'
        )

    def __str__(self):
        return self.recipe.title

    class Meta:
        unique_together = ('shopper', 'recipe')
