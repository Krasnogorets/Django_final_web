from django.shortcuts import render, get_object_or_404
from .forms import AddNewRecipe, RecipeSearchForm
from django.core.files.storage import FileSystemStorage
from .models import Recipe, Category, Ingredients
from random import choices
from django.db.models import Q


def index(request):
    max_carussel_len = 5
    pk_lst = Recipe.objects.exclude(picture__exact='').values_list('id', flat=True)
    if len(pk_lst) <= max_carussel_len:
        pk_rnd = pk_lst
    else:
        pk_rnd = choices(pk_lst, k=5)
    recipes_carussel = {}
    for k, i in enumerate(pk_rnd):
        recipes_carussel[f'set{k}'] = Recipe.objects.filter(pk=i)

    return render(request,
                  'recipes/index.html', {'recipes_carussel': recipes_carussel})


def add_new_recipe(request):
    form = AddNewRecipe(request.POST, request.FILES)
    if request.method == 'POST':

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
            return render(request, 'recipes/add_recipe.html', {'form': form,
                                                               'message': 'Форма недействительна'})

    else:
        form = AddNewRecipe()
        message = 'Заполните форму для рецепта'
        return render(request, 'recipes/add_recipe.html', {'form': form, 'message': message})


def all_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/all_recipes.html', {'recipes': recipes})


def recipes_by_user(request, author_id):
    if author_id:
        recipes = Recipe.objects.filter(author=author_id).order_by('-date_of_creation')
        return render(request, 'recipes/recipes_by_user.html', {'recipes': recipes})


def recipe_full(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.views += 1
    recipe.save()
    category = Category.objects.filter(recipe=recipe).values_list('title', flat=True)
    ingredients = list(Ingredients.objects.filter(recipe=recipe))
    return render(request, 'recipes/recipe_full.html',
                  {'recipe': recipe, 'category': category, 'ingredients': ingredients})


def update_recipe(request, recipe_id):
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
            return render(request, 'recipes/update_recipe.html', {'form': form, 'message': message})

    else:
        recipe = Recipe.objects.get(pk=recipe_id)
        form = AddNewRecipe(instance=recipe)
        message = 'внесите нужные исправления в рецепт'
        return render(request, 'recipes/update_recipe.html', {'form': form, 'message': message})


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    message = 'Рецепт удален'
    return render(request, 'recipes/recipe_full.html', {'message': message})


def search_by_category(request, cat):
    message = None
    categories = Category.objects.all()
    ingredients = list(Ingredients.objects.all())
    cat_id = get_object_or_404(Category, title=cat)
    recipes = Recipe.objects.filter(category=cat_id.pk)
    form = RecipeSearchForm(request.GET)
    if not recipes:
        message = "ничего не найдено"
    search_ref = "категории"
    return render(request, 'recipes/search.html', {'recipes': recipes, 'cat_name': cat,
                                                   'search_ref': search_ref, 'categories': categories,
                                                   'message': message, 'form': form, 'ingredients': ingredients})


def search_by_ingredient(request, ingredient):
    message = None
    categories = Category.objects.all()
    ingredients = list(Ingredients.objects.all())
    ingridient_id = get_object_or_404(Ingredients, title=ingredient)
    recipes = Recipe.objects.filter(ingredients=ingridient_id.pk)
    form = RecipeSearchForm(request.GET)
    if not recipes:
        message = "ничего не найдено"
    search_ref = "ингридиенту"
    return render(request, 'recipes/search.html',
                  {'recipes': recipes, 'cat_name': ingredient, 'form': form, 'search_ref': search_ref,
                   'categories': categories,
                   'message': message,
                   'ingredients': ingredients})


def search(request):
    categories = Category.objects.all()
    ingredients = list(Ingredients.objects.all())
    form = RecipeSearchForm(request.GET)
    message = None
    if request.method == 'POST':
        category_id = request.POST.get('category')
        ingredient_id = request.POST.get('ingredients')
        if category_id:
            cat_name = get_object_or_404(Category, pk=category_id)
            recipes = Recipe.objects.filter(category=cat_name)
            search_ref = "категории"
        elif ingredient_id:
            cat_name = get_object_or_404(Ingredients, pk=ingredient_id)
            recipes = Recipe.objects.filter(ingredients=cat_name)
            search_ref = "ингридиенту"
        else:
            return render(request, 'recipes/search.html',
                          {'form': form, 'categories': categories, 'ingredients': ingredients})
        if not recipes:
            message = "ничего не найдено"
        return render(request, 'recipes/search.html',
                      {'recipes': recipes, 'cat_name': cat_name, 'search_ref': search_ref, 'categories': categories,
                       'ingredients': ingredients, 'message': message, 'form': form})

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            recipes = Recipe.objects.filter(
                Q(title__iregex=query) |
                Q(description__iregex=query) |
                Q(cooking_steps__iregex=query))
        else:
            recipes = None
        if not recipes:
            message = "ничего не найдено"
        cat_name = query
        search_ref = ''
        return render(request, 'recipes/search.html',
                      {'recipes': recipes, 'cat_name': cat_name, 'search_ref': search_ref, 'categories': categories,
                       'ingredients': ingredients, 'form': form, 'message': message})

    return render(request, 'recipes/search.html',
                  {'form': form, 'categories': categories, 'ingredients': ingredients, 'message': message})
