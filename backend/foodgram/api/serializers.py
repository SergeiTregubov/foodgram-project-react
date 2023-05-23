from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe, 
                            ShoppingCart, Tag) 
from rest_framework import serializers 
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from users.models import User
 
 
class CustomUserSerializer(serializers.ModelSerializer): 
    """Сериализатор пользовательской модели.""" 
    is_subscribed = serializers.SerializerMethodField() 
 
    class Meta: 
        model = User 
        fields = ( 
            'email', 'id', 'username', 'first_name', 'last_name', 
            'is_subscribed' 
        ) 
 
    def get_is_subscribed(self, obj): 
        user = self.context.get('request').user 
        return user.is_authenticated and user.subscriber.filter( 
            user=user, author=obj 
        ).exists() 
 
 
class SubscriptionUserSerializer(CustomUserSerializer): 
    """Сериализатор пользователей подписки.""" 
    recipes = serializers.SerializerMethodField() 
    recipes_count = serializers.IntegerField( 
        source='recipes.count', 
        read_only=True 
    ) 
 
    class Meta: 
        model = User 
        fields = ( 
            'email', 'id', 'username', 'first_name', 'last_name', 
            'is_subscribed', 'recipes', 'recipes_count' 
        ) 
 
    def get_recipes(self, obj): 
        request = self.context.get('request')
        if not request.user.is_anonymous:
            context = {'request': request}
            recipes_limit = request.GET.get('recipes_limit')
        else:
            return False   
        if recipes_limit is not None:
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except ValueError:
                raise ValidationError(
                    ('''Параметр исключает тип int''')
                    ) 
        return RecipeShortSerializer(recipes, many=True, context=context).data 
 
 
class IngredientSerializer(serializers.ModelSerializer): 
    """Сериализатор моделей ингредиентов.""" 
 
    class Meta: 
        model = Ingredient 
        fields = '__all__' 
 
 
class TagSerializer(serializers.ModelSerializer): 
    """Сериализатор моделей тегов.""" 
 
    class Meta: 
        model = Tag 
        fields = '__all__' 
 
 
class IngredientAmountSerializer(serializers.ModelSerializer): 
    """Сериализатор модели количества ингредиентов.""" 
    id = serializers.PrimaryKeyRelatedField( 
        queryset=Ingredient.objects.all(), 
        source='ingredient.id' 
    ) 
    name = serializers.CharField( 
        source='ingredient.name', 
        read_only=True 
    ) 
    measurement_unit = serializers.CharField( 
        source='ingredient.measurement_unit', 
        read_only=True 
    ) 
 
    class Meta: 
        model = IngredientAmount 
        fields = ('id', 'name', 'measurement_unit', 'amount') 
 
 
class RecipeSerializer(serializers.ModelSerializer): 
    """Сериализатор модели рецепта.""" 
    tags = TagSerializer( 
        read_only=True, 
        many=True 
    ) 
    author = CustomUserSerializer( 
        read_only=True, 
        default=serializers.CurrentUserDefault() 
    ) 
    ingredients = IngredientAmountSerializer( 
        many=True, 
        source='ingredients_amount' 
    ) 
    is_favorited = serializers.BooleanField(read_only=True) 
    is_in_shopping_cart = serializers.BooleanField(read_only=True) 
    image = Base64ImageField( 
        required=False, 
        allow_null=True 
    ) 
 
    class Meta: 
        model = Recipe 
        fields = ( 
            'id', 'tags', 'author', 'ingredients', 'is_favorited', 
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time' 
        ) 
 
 
class RecipeWriteSerializer(RecipeSerializer): 
    """Сериализатор модели рецепта (создать рецепт).""" 
    tags = serializers.PrimaryKeyRelatedField( 
        many=True, 
        queryset=Tag.objects.all() 
    ) 
 
    class Meta: 
        model = Recipe 
        fields = ( 
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time' 
        ) 
 
    @staticmethod 
    def save_ingredients(recipe, ingredients): 
        ingredients_list = [] 
        for ingredient in ingredients: 
            current_ingredient = ingredient['ingredient']['id'] 
            current_amount = ingredient.get('amount') 
            ingredients_list.append( 
                IngredientAmount( 
                    recipe=recipe, 
                    ingredient=current_ingredient, 
                    amount=current_amount 
                ) 
            ) 
        IngredientAmount.objects.bulk_create(ingredients_list) 
 
    def validate(self, data): 
        cooking_time = data.get('cooking_time') 
        if cooking_time <= 0: 
            raise serializers.ValidationError( 
                { 
                    'error': 'Cooking time cannot be less than minutes' 
                } 
            ) 
        ingredients_list = [] 
        ingredients_amount = data.get('ingredients_amount') 
        for ingredient in ingredients_amount: 
            if ingredient.get('amount') <= 0: 
                raise serializers.ValidationError( 
                    { 
                        'error': 'The ingredients number cannot be less than 1' 
                    } 
                ) 
            ingredients_list.append(ingredient['ingredient']['id']) 
        if len(ingredients_list) > len(set(ingredients_list)): 
            raise serializers.ValidationError( 
                { 
                    'error': 'Ingredients should not be repeated' 
                } 
            ) 
        return data 
 
    def create(self, validated_data): 
        author = self.context.get('request').user 
        ingredients = validated_data.pop('ingredients_amount') 
        tags = validated_data.pop('tags') 
        recipe = Recipe.objects.create(**validated_data, author=author) 
        recipe.tags.add(*tags) 
        self.save_ingredients(recipe, ingredients) 
        return recipe 
 
    def update(self, instance, validated_data): 
        instance.name = validated_data.get('name', instance.name) 
        instance.text = validated_data.get('text', instance.text) 
        instance.image = validated_data.get('image', instance.image) 
        instance.cooking_time = validated_data.get( 
            'cooking_time', 
            instance.cooking_time 
        ) 
        ingredients = validated_data.pop('ingredients_amount') 
        tags = validated_data.pop('tags') 
        instance.tags.clear() 
        instance.tags.add(*tags) 
        instance.ingredients.clear() 
        recipe = instance 
        self.save_ingredients(recipe, ingredients) 
        instance.save() 
        return instance 
 
 
class RecipeShortSerializer(RecipeSerializer): 
    """Сериализатор коротких рецептов.""" 
 
    class Meta: 
        model = Recipe 
        fields = ('id', 'name', 'image', 'cooking_time') 
 
 
class FavoriteSerializer(RecipeShortSerializer): 
    """Сериализатор любимых моделей.""" 
    user = serializers.PrimaryKeyRelatedField( 
        queryset=User.objects.all(), 
        write_only=True, 
    ) 
    recipe = serializers.PrimaryKeyRelatedField( 
        queryset=Recipe.objects.all(), 
        write_only=True, 
    ) 
 
    class Meta: 
        model = Favorite 
        fields = ('user', 'recipe') 
        validators = [ 
            UniqueTogetherValidator( 
                queryset=Favorite.objects.all(), 
                fields=('user', 'recipe'), 
                message='You have already added the recipe to favorites' 
            ) 
        ] 
 
 
class ShoppingCartSerializer(RecipeShortSerializer): 
    """Сериализатор модели корзины покупок.""" 
    user = serializers.PrimaryKeyRelatedField( 
        queryset=User.objects.all(), 
        write_only=True, 
    ) 
    recipe = serializers.PrimaryKeyRelatedField( 
        queryset=Recipe.objects.all(), 
        write_only=True, 
    ) 
 
    class Meta: 
        model = ShoppingCart 
        fields = ('user', 'recipe') 
        validators = [ 
            UniqueTogetherValidator( 
                queryset=ShoppingCart.objects.all(), 
                fields=('user', 'recipe'), 
                message='You have already added the recipe to shopping cart' 
            ) 
        ] 
