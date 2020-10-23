from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    TAG_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ]
    title = models.CharField(max_length=10, choices=TAG_CHOICES)

    def __str__(self):
        return self.title

    @property
    def color(self):
        if self.title == 'breakfast':
            return 'orange'
        if self.title == 'lunch':
            return 'green'
        return 'purple'

    @property
    def name(self):
        if self.title == 'breakfast':
            return 'Завтрак'
        if self.title == 'lunch':
            return 'Обед'
        return 'Ужин'


class Ingredient(models.Model):

    title = models.CharField(max_length=300)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return str(self.title)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_recipes"
        )
    title = models.CharField(max_length=300)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Recipe_Ingredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipe_ingredients'
        )
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='recipe_tags')
    image = models.ImageField(
        upload_to='recipe/', default='default/default_img.jpg')

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-pub_date']

    def get_ingredients(self):
        return "\n".join([i.title for i in self.ingredients.all()])
    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self):
        return "\n".join([t.title for t in self.tags.all()])
    get_tags.short_description = 'Тэги'


class Recipe_Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes_quantity"
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        )
    quantity = models.FloatField()

    def __str__(self):
        return str(self.ingredient)


class Cart(models.Model):
    shopper = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipes'
        )

    def __str__(self):
        return self.recipe.title

    class Meta:
        unique_together = ('shopper', 'recipe')
