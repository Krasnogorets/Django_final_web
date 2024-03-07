from django.urls import path
from django.contrib.auth import views as auth_views
from user_app import views

app_name = 'user_app'
urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user_app/logout.html'), name='logout'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
]
