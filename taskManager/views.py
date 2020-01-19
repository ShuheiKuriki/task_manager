from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TaskForm, UserForm
from .models import Task, Done

def index(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks':tasks})

def form(request):
    form = TaskForm()
    return render(request, 'form.html', {'form': form})

def post(request):
    if request.method != 'POST':
        return redirect(to="/form")
    form = TaskForm(request.POST)
    if form.is_valid():
        task=Task.objects.create(name=request.POST.get('タスク名'))
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
    if request.method == 'POST' and request.POST['id'] and request.POST['name']:
        done = Done.objects.create(name=request.POST['name'])
        task = Task.objects.get(id=request.POST['id'])
        task.delete()
        return redirect(to='/')

def done_view(request):
    dones = Done.objects.all()
    return render(request, 'done.html', {'dones':dones})

def edit(request):
    if request.method == 'POST' and request.POST['id']:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(id=request.POST['id'])
            task.name = request.POST['タスク名']
            task.save()
    return redirect(to='/')

def edit_view(request):
    if request.method == 'POST' and request.POST.get('id'):
        id = request.POST.get('id')
    form = TaskForm()
    return render(request, 'edit.html', {'form': form, 'id': id})

def recover(request):
    if request.method == 'POST' and request.POST['id'] and request.POST['name']:
        task = Task.objects.create(name=request.POST['name'])
        done = Done.objects.get(id=request.POST['id'])
        done.delete()
    return redirect('/')

def today(request):
    return none

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
