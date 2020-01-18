from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import Task

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
        task=Task.objects.create(name=request.POST.get('name'), id=request.POST.get('id'))
        task.save()
        return redirect(to='/')
    else:
        return redirect(to='/form')

def delete(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.delete()
    return redirect(to='/')
