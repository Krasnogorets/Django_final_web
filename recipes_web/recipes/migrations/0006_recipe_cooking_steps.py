# Generated by Django 5.0.2 on 2024-02-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_recipe_qts_type_remove_recipe_qts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cooking_steps',
            field=models.TextField(default='', verbose_name='Шаги готовки'),
        ),
    ]
