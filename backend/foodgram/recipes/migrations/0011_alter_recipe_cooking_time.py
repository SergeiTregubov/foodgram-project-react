# Generated by Django 3.2.19 on 2023-05-18 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20230518_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='в минутах', validators=[django.core.validators.MinValueValidator(1, message='Минимальное время приготовлениядолжно быть больше или равно 1 мин!')], verbose_name='Время приготовления'),
        ),
    ]
