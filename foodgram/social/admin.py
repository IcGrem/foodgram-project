from django.contrib import admin
from .models import Comment, Follow, Favorit


class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "text", "author", "created",)
    search_fields = ("text",)
    list_filter = ("created",)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author",)
    search_fields = ("user",)
    list_filter = ("user",)
    empty_value_display = '-пусто-'


class FavoritAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe",)
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorit, FavoritAdmin)
