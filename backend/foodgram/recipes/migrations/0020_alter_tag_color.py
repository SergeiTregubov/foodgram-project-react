# Generated by Django 3.2.19 on 2023-05-23 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_auto_20230522_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='example, #49B64E', max_length=7, unique=True, validators=[django.core.validators.RegexValidator('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', 'код цвета в HEX-формате: #ff0000')], verbose_name='Цвет'),
        ),
    ]