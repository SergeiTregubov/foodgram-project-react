import django_filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов."""
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецептов."""
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="Ссылка",
    )
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=Recipe.objects.all(),
        field_name="author__id",
        to_field_name="id",
    )
    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='В избранных'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
