from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import AddNewRecipe
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .models import Recipe, Category, Ingredients
from random import choices


def index(request):
    max_carussel_len = 5
    pk_lst = Recipe.objects.exclude(picture__exact='').values_list('id', flat=True)
    print(pk_lst)
    if len(pk_lst) <= max_carussel_len:
        pk_rnd = pk_lst
    else:
        pk_rnd = choices(pk_lst, k=5)
    print(pk_rnd)
    recipes_carussel = {}
    for k, i in enumerate(pk_rnd):
        recipes_carussel[f'set{k}'] = Recipe.objects.filter(pk=i)

    return render(request,
                  'recipes/index.html', {'recipes_carussel': recipes_carussel})


def about(request):
    return HttpResponse("About us")


def add_new_recipe(request):
    if request.method == 'POST':
        form = AddNewRecipe(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                picture = form.cleaned_data['picture']
                fs = FileSystemStorage()
                fs.save(picture.name, picture)
            else:
                picture = None
            title = form.cleaned_data['title']
            author = request.user
            description = form.cleaned_data['description']
            ingredients = form.cleaned_data['ingredients']
            category = form.cleaned_data['category']
            cooking_time = form.cleaned_data['cooking_time']
            cooking_steps = form.cleaned_data['cooking_steps']
            recipe = Recipe.objects.create(title=title, picture=picture,
                                           author=author, description=description,
                                           cooking_time=cooking_time, cooking_steps=cooking_steps)
            recipe.ingredients.add(*ingredients)
            recipe.category.add(*category)
            message = 'рецепт добавлен в бд'
            return render(request, 'recipes/add_recipe.html', {'form': form, 'message': message})
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form, 'message': 'Форма недействительна'})

    else:
        form = AddNewRecipe()
        message = 'Заполните форму для рецепта'
        return render(request, 'recipes/add_recipe.html', {'form': form, 'message': message})


def all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/all_recipes.html', {'recipes': recipes})


def recipes_by_user(request, author_id):
    recipes = Recipe.objects.filter(author=author_id).order_by('-date_of_creation')
    return render(request, 'recipes/recipes_by_user.html', {'recipes': recipes})


def recipe_full(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.views += 1
    recipe.save()
    category = Category.objects.filter(recipe=recipe).values_list('title', flat=True)
    ingredients = list(Ingredients.objects.filter(recipe=recipe))
    # print(ingredients)
    return render(request, 'recipes/recipe_full.html', {'recipe': recipe, 'category':category, 'ingredients':ingredients})



def update_recipe(request,recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id).first()
    if request.method == 'POST':
        form = AddNewRecipe(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            if request.FILES:
                picture = form.cleaned_data['picture']
                fs = FileSystemStorage()
                fs.save(picture.name, picture)
            else:
                picture = recipe.picture
            recipe.picture = picture
            recipe.title = form.cleaned_data['title']
            recipe.description = form.cleaned_data['description']
            ingredients = form.cleaned_data['ingredients']
            category = form.cleaned_data['category']
            recipe.cooking_time = form.cleaned_data['cooking_time']
            recipe.cooking_steps = form.cleaned_data['cooking_steps']
            recipe.save()
            recipe.ingredients.add(*ingredients)
            recipe.category.add(*category)
            message = 'рецепт обновлен !'
            form = AddNewRecipe(instance=recipe)
            return render(request, 'recipes/update_recipe.html', {'form': form,'message': message})

    else:
        recipe = Recipe.objects.get(pk=recipe_id)
        form = AddNewRecipe(instance=recipe)
        message = 'внесите нужные исправления в рецепт'
        return render(request, 'recipes/update_recipe.html', {'form': form, 'message': message})