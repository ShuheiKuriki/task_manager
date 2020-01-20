from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TaskForm, UserForm
from .models import Task
import datetime

def index(request):
    tasks = Task.objects.all().filter(done_or_not=False).order_by('deadline').order_by('when')
    return render(request, 'index.html', {'tasks':tasks})

def form(request):
    form = TaskForm()
    return render(request, 'form.html', {'form': form})

def post(request):
    if request.method != 'POST':
        return redirect(to="/form")
    form = TaskForm(request.POST)
    if form.is_valid():
        task=Task.objects.create(name=request.POST.get('name'), deadline=request.POST.get('deadline'))
        task.save()
        return redirect(to='/')
    else:
        return redirect(to='/form')

def delete(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.delete()
    return redirect(to='/')

def done(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.done_or_not = True
        task.save()
        return redirect(to='/')

def done_view(request):
    dones = Task.objects.all().filter(done_or_not=True)
    return render(request, 'done.html', {'dones':dones})

def edit(request):
    if request.method == 'POST' and request.POST['id']:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(id=request.POST['id'])
            if request.POST['name']!="":
                task.name = request.POST['name']
            if request.POST['deadline']!="":
                task.deadline = request.POST['deadline']
            if request.POST['when']!="":
                task.when = request.POST['when']
            task.save()
    return redirect(to='/')

def edit_view(request):
    if request.method == 'POST' and request.POST.get('id'):
        id = request.POST['id']
    form = TaskForm()
    return render(request, 'edit.html', {'form': form, 'id': id})

def recover(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.done_or_not = False
        task.save()
    return redirect('/')

def today(request):
    tasks = Task.objects.all().filter(done_or_not=False, when=datetime.date.today())
    num = len(tasks)
    return render(request, 'today.html', {'tasks':tasks,'num':num})

def login_view(request):
    user=authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )
    if user is not None:
        login(request,user)
        return redirect('/')
    else:
        return redirect('accounts/login')

def create_user_view(request):
    form=UserForm()
    return render(request,'create_user_view.html', {'form':form})

def create_user(request):
    user=User.objects.create_user(
        request.POST.get('username'),
        request.POST.get('email'),
        request.POST.get('password')
    )
    user.save()
    return redirect('/accounts/login/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
