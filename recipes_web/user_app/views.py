from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from user_app.forms import LoginForm, RegistrationForm


class MyLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_app/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def get_success_url(self):
        return reverse_lazy('recipes:index')


class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_app/signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy('user_app:login')

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='повара')
        user.groups.add(group)
        return super().form_valid(form)
