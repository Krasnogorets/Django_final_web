# Generated by Django 5.0.2 on 2024-02-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_recipe_cooking_steps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_steps',
            field=models.TextField(default='', verbose_name='Шаги приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название рецепта'),
        ),
    ]