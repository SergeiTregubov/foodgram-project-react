# Generated by Django 3.2.19 on 2023-05-17 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230517_1537'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['user', 'author'], 'verbose_name': 'Подписчик', 'verbose_name_plural': 'Subscriptions'},
        ),
    ]
