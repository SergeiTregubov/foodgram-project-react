from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .paginator import LimitPageNumberPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          RecipeWriteSerializer, ShoppingCartSerializer,
                          SubscriptionUserSerializer, TagSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    pagination_class = LimitPageNumberPagination

    @action(methods=('POST', 'DELETE'), detail=True)
    def subscribe(self, request, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = get_object_or_404(self.queryset, id=kwargs.get('id'))
        serializer = SubscriptionUserSerializer(
            obj, context={'request': request}
        )
        if self.request.method == 'POST':
            user.subscribe.add(obj)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if self.request.method == 'DELETE':
            user.subscribe.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = SubscriptionUserSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Список ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Список тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Список рецептов."""
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('favorite', 'shopping_cart'):
            return RecipeShortSerializer
        if self.action in ('create', 'partial_update'):
            return RecipeWriteSerializer
        return RecipeSerializer
    
    def get_queryset(self): 
        user_id = self.request.user.pk 
        return Recipe.objects.add_user_annotations(user_id).select_related( 
            'author' 
        ).prefetch_related( 
            'ingredients', 'tags' 
        )

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'user': user.pk,
            'recipe': recipe.pk
        }
        serializer = FavoriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        message = {
            'detail': 'You have successfully unfavorited'
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthorOrAdminOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            'user': user.pk,
            'recipe': recipe.pk
        }
        serializer = ShoppingCartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        message = {
            'detail':
                'You have successfully removed recipe from shopping cart'
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')).annotate(
            amount=Sum('amount')
        )
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["measurement_unit"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        filename = 'shopping_cart.txt'
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request
