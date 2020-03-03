# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm
from taskManager.models import Task, LinePush
from taskManager.views import Taskinfo

import datetime

class Login(LoginView):
    #ログインページ
    form_class = LoginForm
    template_name = 'Form/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    #ログアウトページ
    template_name = 'Form/login.html'

def profile(request):
    return redirect('/accounts/'+str(request.user.id))

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'Form/signup.html'

# ユーザーに固有の一覧ページ
def index(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    today = Taskinfo(
        name="今日",
        tasks=tasks.filter(when__lte=datetime.date.today()).order_by('order')
    )
    tom = Taskinfo(
        name="明日",
        tasks=tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
    )
    other = Taskinfo(
        name="明日以降",
        tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when')
    )
    infos = [today, tom, other]
    return render(request, 'Menu/list/all_list.html', {'infos':infos})

def today(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    info = Taskinfo(tasks=tasks.filter(when__lte=datetime.date.today()).order_by('order'))
    infos = [info]
    return render(request, 'Menu/list/today.html', {'infos':infos})

def tomorrow(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    info = Taskinfo(tasks=tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order'))
    infos = [info]
    return render(request, 'Menu/list/tomorrow.html', {'infos':infos})

def done_list(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    week = Taskinfo(tasks = dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7)))
    data = []
    for i in range(7):
        info = Taskinfo(tasks = dones.filter(done_date=datetime.date.today()-datetime.timedelta(days=i)))
        data.append(info.num)
    return render(request, 'Menu/done.html', {'week':week, 'today':data[0], 'data':data})
