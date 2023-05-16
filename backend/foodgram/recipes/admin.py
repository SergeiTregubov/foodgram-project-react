from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель ингредиентов в админ."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Модель тегов в админ"""
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель рецепта в админ."""
    list_display = ('name', 'author', 'text', 'added_to_favorite')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInline,)

    @staticmethod
    def added_to_favorite(obj):
        return obj.favorite.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Модель избранное в админ."""
    list_display = ('id', 'recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель корзины покупок в админ."""
    list_display = ('id', 'recipe', 'user')


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Модель количества ингредиентов в админ."""
    list_display = ('id', 'ingredient', 'recipe', 'amount')
