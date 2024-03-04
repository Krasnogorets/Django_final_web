from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}'


class Ingredients(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title}'


class Recipe(models.Model):
    title = models.CharField(max_length=200, unique=True,
                             verbose_name="Название рецепта")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Автор рецепта")
    description = models.TextField(default="",
                                   verbose_name="Краткое описание")
    cooking_steps = models.TextField(default="",
                                     verbose_name="Шаги приготовления")
    ingredients = models.ManyToManyField(Ingredients,
                                         verbose_name="Ингридиенты")

    category = models.ManyToManyField(Category,
                                      verbose_name="Категория")
    cooking_time = models.IntegerField(default=0,
                                       verbose_name="Время готовки")
    picture = models.ImageField(null=True, blank=True, upload_to="recipes_img/", verbose_name='Изображение')
    views = models.IntegerField(default=0,
                                verbose_name="Количество просмотров")
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name="Время создания")
    date_of_update = models.DateTimeField(auto_now=True,
                                          verbose_name="Обновлено")

    def picture_view(self):
        return format_html(
            '<img src="{}" style="max-width:100px; max-height:100px">'.format(self.picture.url))

    def __str__(self):
        return self.title

