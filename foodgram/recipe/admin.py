from django.contrib import admin
from .models import Recipe, Ingredient, Recipe_Ingredient, Tag, Cart


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "description",
        "get_ingredients",
        "cooking_time",
        "pub_date",
        "get_tags",
        "image",
        )
    inlines = [IngredientsInline, ]
    exclude = ('ingredients',)
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension",)
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "color",
        "name",
        )
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


class Recipe_IngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity",)
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ("recipe", "shopper",)
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe_Ingredient, Recipe_IngredientAdmin)
admin.site.register(Cart, CartAdmin)
