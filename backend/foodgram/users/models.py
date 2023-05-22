from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользовательская модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        max_length=settings.MAX_EMAIL_NAME_LENGTH,
        unique=True,
        verbose_name='Email',
        help_text='Введите электронную почту пользователя'
    )
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH_FIRST_NAME,
        verbose_name='Имя',
        help_text='Введите имя пользователя'
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH_LAST_NAME,
        verbose_name='Фамилия',
        help_text='Введите фамилию пользователя'
    )
    

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Подписка на автора рецептурной модели."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['user', 'author']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_subscription',
                check=~models.Q(user=models.F('author')),
            )
        ]

    def __str__(self):
        return f'{self.user} subscribed on {self.author}'
