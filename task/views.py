from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .forms import TaskCreateForm, TaskUpdateForm, DoneEditForm
from taskManager.models import Task

import datetime
# Create your views here.
class Taskinfo:
    def __init__(self, tasks, name=""):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        n = int((self.num*2)**(1/2))
        if n*(n+1)/2 <= self.num:
            self.level = n
        else:
            self.level = n-1

def index(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    past_tasks = tasks.filter(when__lt=datetime.date.today())
    for past_task in past_tasks:
        past_task.when = datetime.date.today()
        past_task.save()
    for task in tasks:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    today = Taskinfo(name="今日",
        tasks=tasks.filter(when=datetime.date.today()).order_by('order'))
    tom = Taskinfo(name="明日",
        tasks=tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('expired').order_by('order'))
    other = Taskinfo(name="明日以降",
        tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('expired').order_by('when'))
    infos = [today, tom, other]
    return render(request, 'task/list/all_list.html', {'infos':infos})

def today(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when__lte=datetime.date.today())
    for task in tasks:
        task.when = datetime.date.today()
        task.save()
    for task in tasks:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    num = len(tasks)
    names = ['~12時','12~15時','15~18時','18~21時','21時~']
    infos = []
    for i,name in enumerate(names):
        info = Taskinfo(name=name, tasks=tasks.filter(period=i).order_by('order'))
        infos.append(info)
    return render(request, 'task/list/today.html', {'infos':infos, 'num':num})

def tomorrow(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1))
    for task in tasks:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    num = len(tasks)
    names = ['~12時','12~15時','15~18時','18~21時','21時~']
    infos = []
    for i,name in enumerate(names):
        info = Taskinfo(name=name, tasks=tasks.filter(period=i).order_by('order'))
        infos.append(info)
    return render(request, 'task/list/tomorrow.html', {'infos':infos, 'num':num})

def done_list(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    week = Taskinfo(tasks = dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7)))
    data = []
    for i in range(7):
        info = Taskinfo(tasks = dones.filter(done_date=datetime.date.today()-datetime.timedelta(days=i)))
        data.append(info.num)
    return render(request, 'task/list/done_list.html', {'week':week, 'today':data[0], 'data':data})

#未完了タスク関連
def create(request):
    if request.method == 'GET':
        form = TaskCreateForm()
        next = request.GET.get('next')
        return render(request, 'task/create.html', {'form': form,'next': next})
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        repeat = int(request.POST.get('repeat'))
        num = int(request.POST.get('num'))
        deadline = datetime.datetime.strptime(request.POST.get('deadline'), '%Y-%m-%d')
        when = datetime.datetime.strptime(request.POST.get('when'), '%Y-%m-%d')
        tasks = []
        if form.is_valid():
            for i in range(num):
                task=Task(
                    name=request.POST.get('name'),
                    deadline=deadline.strftime('%Y-%m-%d'),
                    period=request.POST.get('period'),
                    when=when.strftime('%Y-%m-%d'),
                    important=form.cleaned_data['important'],
                    urgent=form.cleaned_data['urgent'],
                    user=request.user
                )
                tasks.append(task)
                when += datetime.timedelta(days=repeat)
                deadline += datetime.timedelta(days=repeat)
        Task.objects.bulk_create(tasks)
        return redirect_to_origin(request)

@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return original_url(self)

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        context['task'] = context['object'].get_list()
        return context

    def get_success_url(self):
        return original_url(self)

@login_required
def later(request, pk):
    task = Task.objects.get(id=pk)
    task.when += datetime.timedelta(days=1)
    task.save()
    return redirect('task:list', pk=request.user.id)

@login_required
def period_before(request, pk):
    task = Task.objects.get(id=pk)
    if task.period > 0:
        task.period -= 1
    task.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:today', pk=request.user.id)

@login_required
def period_after(request, pk):
    task = Task.objects.get(id=pk)
    if task.period == 4:
        task.when += datetime.timedelta(days=1)
        task.period = 0
    else:
        task.period += 1
    task.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:today', pk=request.user.id)

@csrf_exempt
def sort(request):
    for order, id in enumerate(request.POST.getlist('task[]')):
        task = Task.objects.get(id=id)
        task.order = order
        task.save()
    return HttpResponse('')

# 完了タスク関連の操作
@login_required
def done(request, pk):
    task = Task.objects.get(id=pk)
    task.done_or_not = True
    task.done_date = datetime.date.today()
    task.save()
    return redirect('task:done_list', pk=request.user.id)

@method_decorator(login_required, name='dispatch')
class DoneUpdateView(UpdateView):
    model = Task
    form_class = DoneEditForm
    template_name = 'task/done_update.html'

    def get_success_url(self):
        return reverse_lazy('task:done_list', kwargs={'pk': self.request.user.id})

@login_required
def done_before(request, pk):
    task = Task.objects.get(id=pk)
    task.done_date -= datetime.timedelta(days=1)
    task.save()
    return redirect('task:done_list', pk=request.user.id)

@login_required
def done_after(request, pk):
    task = Task.objects.get(id=pk)
    task.done_date += datetime.timedelta(days=1)
    task.save()
    return redirect('task:done_list', pk=request.user.id)

@login_required
def recover(request, pk):
    task = Task.objects.get(id=pk)
    task.done_or_not = False
    task.save()
    return redirect('task:list', pk=request.user.id)

def redirect_to_origin(request):
    redirect_to = request.GET.get('next')
    url_is_safe = is_safe_url(
        url=redirect_to,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=request.is_secure(),
    )
    if url_is_safe and redirect_to:
        return redirect(redirect_to)

def original_url(self):
    url = self.request.GET.get('next')
    url_is_safe = is_safe_url(
        url=url,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=self.request.is_secure(),
    )
    if url_is_safe and url:
        return url