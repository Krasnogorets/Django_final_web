# Generated by Django 5.0.2 on 2024-02-26 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=11)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]