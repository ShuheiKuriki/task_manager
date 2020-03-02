# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . forms import LoginForm

class Login(LoginView):
    #ログインページ
    form_class = LoginForm
    template_name = 'Form/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    #ログアウトページ
    template_name = 'Form/login.html'


def profile(request):
    return redirect('/accounts'+str(request.user.id))


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'Form/signup.html'

