# Generated by Django 5.0.2 on 2024-02-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_weighttype_remove_ingredients_qts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='qts_type',
            field=models.ManyToManyField(to='recipes.weighttype', verbose_name='Ед. измерения ингридиента'),
        ),
    ]
