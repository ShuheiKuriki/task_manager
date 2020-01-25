from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import TaskForm, UserForm, DoneEditForm
from .models import Task
import datetime

def index(request):
    return render(request, 'index.html')

def login_view(request):
    user=authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )
    if user is not None:
        login(request,user)
        url='/'+str(request.user.id)
        return redirect(url)
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

@login_required
def post(request):
    num = str(request.user.id)
    url = '/'+num
    form_url = '/'+num+'/form'
    if request.method != 'POST':
        return redirect(to=form_url)
    form = TaskForm(request.POST)
    if form.is_valid():
        task=Task.objects.create(
            name=request.POST.get('name'),
            deadline=request.POST.get('deadline'),
            when=request.POST.get('when'),
            user=request.user
            )
        task.save()
        return redirect(to=url)
    else:
        return redirect(to=form_url)

@login_required
def delete(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.delete()
    return redirect(to='/'+str(request.user.id))

@login_required
def done(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.done_or_not = True
        task.done_date = datetime.date.today()
        task.save()
    return redirect(to='/'+str(request.user.id)+'/done_view')

@login_required
def done_edit(request):
    if request.method != 'POST':
        return redirect(to='/'+str(request.user.id)+'/done_view')
    form = DoneEditForm(request.POST)
    if form.is_valid():
        task = Task.objects.get(id=request.POST['id'])
        task.done_date = request.POST['done_date']
        task.save()
    return redirect(to='/'+str(request.user.id)+'/done_view')

@login_required
def recover(request):
    if request.method == 'POST' and request.POST['id']:
        task = Task.objects.get(id=request.POST['id'])
        task.done_or_not = False
        task.save()
    return redirect('/'+str(request.user.id))

@login_required
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
    return redirect(to='/'+str(request.user.id))
# class UserOnlyMixin(UserPassesTestMixin):
#     raise_exception = True
#
#     def test_func(self):
#         user = self.request.user
#         return user.pk == self.kwargs['pk'] or user.is_superuser
#
# class OnlyYouMixin(UserOnlyMixin):

def list(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    tasks_today = tasks.filter(when__lte=datetime.date.today()).order_by('deadline')
    tasks_tom = tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('deadline')
    tasks = tasks.filter(user=request.user, done_or_not=False, when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when')
    num_today = len(tasks_today)
    num_tom = len(tasks_tom)
    return render(request, 'list.html', {'tasks':tasks, 'tasks_today':tasks_today, 'tasks_tom':tasks_tom, 'num_today':num_today, 'num_tom':num_tom})

def form(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    form = TaskForm()
    return render(request, 'form.html', {'form': form})

def done_view(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    done_today = dones.filter(done_date=datetime.date.today())
    done_yes = dones.filter(done_date=datetime.date.today()-datetime.timedelta(days=1))
    dones = dones.filter(done_date__lt=datetime.date.today()-datetime.timedelta(days=1))
    num_today = len(done_today)
    num_yes = len(done_yes)
    if num_today == 0:
        message = '昨日は{}個のタスクをこなしました。今日も頑張りましょう！'.format(num_yes)
    else:
        message = '今日は{}個のタスクをこなしました。よく頑張りましたね！'.format(num_today)
    return render(request, 'done.html', {'dones':dones, 'done_today':done_today, 'done_yes':done_yes, 'num_today':num_today, 'num_yes':num_yes, 'message':message})

def done_edit_view(request):
    if request.method == 'POST' and request.POST.get('id'):
        id = request.POST['id']
        form = DoneEditForm()
        return render(request, 'done_edit.html', {'form': form, 'id': id})
    return redirect('login')

def edit_view(request):
    if request.method == 'POST' and request.POST.get('id'):
        id = request.POST['id']
        form = TaskForm()
        return render(request, 'edit.html', {'form': form, 'id': id})
    return redirect('login')

def today(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when=datetime.date.today()).order_by('deadline')
    num = len(tasks)
    if num == 0:
        message = '今日のタスクは完了です！ゆっくり休みましょう！'
    else:
        message = '今日のタスクはあと{}個です！頑張りましょう！'.format(num)
    return render(request, 'today.html', {'tasks':tasks,'message':message})

def tomorrow(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1)).order_by('deadline')
    num = len(tasks)
    if num == 0:
        message = '明日は自由に過ごしましょう！'
    else:
        message = '明日のタスクは{}個です！明日も頑張りましょう！'.format(num)
    return render(request, 'tomorrow.html', {'tasks':tasks,'message':message})
