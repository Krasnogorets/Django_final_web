from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_recipe/', views.add_new_recipe, name='add_recipe'),
    path('update_recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
    path('recipes/<int:author_id>/', views.recipes_by_user, name='recipes_by_user'),
    path('recipe/<int:recipe_id>/', views.recipe_full, name='recipe_full'),
]

