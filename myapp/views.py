from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import User
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.views import View


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(View):
    template_name = 'logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return LogoutView.as_view(next_page=reverse_lazy('login'))(request)


class HomeView(TemplateView):
    template_name = 'home.html'
