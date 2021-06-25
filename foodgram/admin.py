from django.contrib import admin

from .models import (Favorites, Ingredients, ShopList,
                     Recipe, Tag)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    autocomplete_fields = ('ingredient', )
    min_num = 1


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'dimension')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    def count_favorites(self, obj):
        return obj.Favorites_recipes.count()

    count_favorites.short_description = 'В избранном'

    inlines = (IngredientInline, )
    list_display = ('pk', 'name', 'author', 'count_favorites')
    search_fields = ('name', 'author__username')
    autocomplete_fields = ('author',)
    list_filter = ('pub_date',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingestion', 'color')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')


admin.site.register(ShopList, ShopListAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
