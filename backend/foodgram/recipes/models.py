from django.conf import settings
from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        blank=False,
        max_length=settings.MAX_LENGTH_INGREDIENT_NAME,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        blank=False,
        max_length=settings.MAX_LENGTH_INGREDIENT_MEASURMENT_UNIT,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_NAME,
        unique=True,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=settings.MAX_LENGTH_TAG_COLOR,
        unique=True,
        verbose_name='Цвет',
        help_text='example, #49B64E',
        validators=(
            validators.RegexValidator(
                '^#([A-Fa-f0-9]{6})$',
                'код цвета в HEX-формате: #ff0000'),
        )
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный слаг',
        help_text='Unique URL for the Tag',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPE_NAME,
        unique=True,
        verbose_name='Название',
    )
    image = models.ImageField(
        blank=True,
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='в минутах',
        validators=[MinValueValidator(
            1,
            message='Минимальное время приготовления'
                    'должно быть больше или равно 1 мин!')]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель количества ингредиентов."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.ingredient}: {self.amount}'


class Favorite(models.Model):
    """Модель избранное."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    """Модель корзины для покупок."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Список товара'
        verbose_name_plural = 'Списки товаров'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1!')]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount} '
        )
    