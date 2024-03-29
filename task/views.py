from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, UpdateView
from django.conf import settings

from urllib.parse import urlencode
from .forms import TaskCreateForm, TaskUpdateForm, DoneForm, RoutineForm, RoutineUpdateForm
from taskManager.models import Task
from .models import Routine, AddRoutine

import datetime
from datetime import date


# Create your views here.
class Taskinfo:
    def __init__(self, tasks, name="", day=-1, days=1):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        self.total_h = sum(task.time for task in tasks)
        self.mean_h = int(self.total_h / days * 10) / 10
        if day == -1:
            self.date = ''
        else:
            day_delta = date.today()+datetime.timedelta(days=day)
            week_day = ['月', '火', '水', '木', '金', '土', '日']
            self.date = "{}/{}({})".format(day_delta.month, day_delta.day, week_day[day_delta.weekday()])
        n = int((self.num*2)**(1/2))
        if n*(n+1)/2 <= self.num:
            self.level = n
        else:
            self.level = n-1


class Routineinfo:
    def __init__(self, routines, name=""):
        self.name = name
        self.routines = routines
        self.num = len(routines)
        self.total_h = sum(routine.time for routine in routines)


def list(request, pk):
    if request.user.pk != pk:
        return redirect('account_login')
    d = datetime.date.today()
    day = datetime.datetime.now().weekday()
    if len(AddRoutine.objects.filter(user=request.user)):
        addroutine = AddRoutine.objects.get(user=request.user)
        if addroutine.last_visited != d and addroutine.add_or_not:
            routines = Routine.objects.filter(user=request.user)
            routine_tasks = []
            for routine in routines:
                if routine.days > 0 and routine.days-1 != day:
                    continue
                task = Task(
                    name=routine.name,
                    deadline=d,
                    period=routine.period,
                    when=d,
                    time=routine.time,
                    fixed=routine.fixed,
                    user=request.user
                )
                routine_tasks.append(task)
            Task.objects.bulk_create(routine_tasks)
            addroutine.last_visited = d
            addroutine.save()
    tasks = Task.objects.filter(user=request.user, done_or_not=False)
    todays = tasks.filter(when__lte=datetime.date.today())
    for task in todays:
        task.when = date.today()
        task.save()
    for task in todays:
        task.expired = True if task.deadline < datetime.date.today() else False
        task.save()
    today_num = len(todays)
    names = ['~12時', '12~15時', '15~18時', '18~21時', '21時~']
    h = datetime.datetime.now().hour
    p = max(h//3-3, 0)
    today_infos = []
    for i, name in enumerate(names):
        if i < p:
            continue
        elif i == p:
            info = Taskinfo(name=name, tasks=todays.filter(period__lte=i).order_by('order'))
        else:
            info = Taskinfo(name=name, tasks=todays.filter(period=i).order_by('order'))
        if info.num > 0:
            today_infos.append(info)
    toms = tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1))
    for task in toms:
        task.expired = True if task.deadline < datetime.date.today() else False
        task.save()
    tom_num = len(toms)
    tom_infos = []
    for i, name in enumerate(names):
        info = Taskinfo(name=name, tasks=toms.filter(period=i).order_by('order'))
        if info.num > 0:
            tom_infos.append(info)
    other = Taskinfo(
        name="明日以降",
        tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when')
    )
    return render(request, 'task/task_list.html', {
        'today_infos': today_infos,
        'today_num': today_num,
        'tom_infos': tom_infos,
        'tom_num': tom_num,
        'other': other
    })


def routine_list(request, pk):
    if request.user.pk != pk:
        return redirect('account_login')
    routines = Routine.objects.filter(user=request.user)
    names = ['~12時', '12~15時', '15~18時', '18~21時', '21時~']
    days = ['月', '火', '水', '木', '金', '土', '日']
    daily_infos = []
    for i, name in enumerate(names):
        info = Routineinfo(name=name, routines=routines.filter(days=0, period=i))
        if info.num > 0:
            daily_infos.append(info)
    weekly_infos = []
    for d, day in enumerate(days):
        info = Routineinfo(name=day+"曜", routines=routines.filter(days=1+d).order_by('period'))
        if info.num > 0:
            weekly_infos.append(info)
    if len(AddRoutine.objects.filter(user=request.user)):
        add_or_not = AddRoutine.objects.get(user=request.user).add_or_not
    else:
        add_or_not = False
    return render(request, 'task/routine_list.html', {
        'daily_infos': daily_infos,
        'weekly_infos': weekly_infos,
        'add_or_not': add_or_not
    })


def done_list(request, pk):
    if request.user.pk != pk:
        return redirect('account_login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    week = Taskinfo(tasks=dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7)), days=7)
    month = Taskinfo(tasks=dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=30)), days=30)
    nums = []
    hours = []
    for i in range(29, -1, -1):
        dat = date.today()-datetime.timedelta(days=i)
        info = Taskinfo(tasks=dones.filter(done_date=dat))
        nums.append(info.num)
        hours.append(int(info.total_h*10)*0.1)
    return render(request, 'task/done_list.html', {
        'week': week,
        'month': month,
        'today': nums[-1],
        'nums': nums,
        'hours': hours
    })


# 未完了タスク関連
def create(request):
    if request.method == 'GET':
        form = TaskCreateForm()
        nex = request.GET.get('next')
        return render(request, 'task/task_create.html', {'form': form, 'next': nex})
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        repeat = int(request.POST.get('repeat'))
        num = int(request.POST.get('num'))
        deadline = datetime.datetime.strptime(request.POST.get('deadline'), '%Y-%m-%d')
        when = datetime.datetime.strptime(request.POST.get('when'), '%Y-%m-%d')
        tasks = []
        if form.is_valid():
            for i in range(num):
                task = Task(
                    name=request.POST.get('name'),
                    deadline=deadline.strftime('%Y-%m-%d'),
                    period=request.POST.get('period'),
                    when=when.strftime('%Y-%m-%d'),
                    time=form.cleaned_data['time'],
                    fixed=form.cleaned_data['fixed'],
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
    template_name = 'task/task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return original_url(self)


@require_POST
def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect_to_origin(request)


@login_required
def later(request, pk):
    task = Task.objects.get(id=pk)
    task.when += datetime.timedelta(days=1)
    task.save()
    return redirect_to_origin(request)


@login_required
def period_before(request, pk):
    task = Task.objects.get(id=pk)
    task.period -= 1
    task.period %= 5
    task.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:today', pk=request.user.id)


@login_required
def period_after(request, pk):
    task = Task.objects.get(id=pk)
    if task.when == datetime.date.today():
        h = datetime.datetime.now().hour
        p = max(h//3-3, 0)
        if task.period < p:
            task.period = p
    task.period += 1
    task.period %= 5
    task.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:today', pk=request.user.id)


@csrf_exempt
def sort(request):
    print(request.POST.getlist('task[]'))
    for order, _id in enumerate(request.POST.getlist('task[]')):
        print(order, _id)
        task = Task.objects.get(id=_id)
        task.order = order
        task.save()
    return HttpResponse('')


# ルーティン関連
@method_decorator(login_required, name='dispatch')
class RoutineCreateView(CreateView):
    form_class = RoutineForm
    template_name = 'task/routine_create.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(RoutineCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task:routine_list', kwargs={'pk': self.request.user.id})


@method_decorator(login_required, name='dispatch')
class RoutineUpdateView(UpdateView):
    model = Routine
    form_class = RoutineUpdateForm
    template_name = 'task/routine_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return reverse_lazy('task:routine_list', kwargs={'pk': self.request.user.id})


@require_POST
def routine_delete(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    routine.delete()
    return redirect_to_origin(request)


@login_required
def routine_before(request, pk):
    routine = Routine.objects.get(id=pk)
    routine.period -= 1
    routine.period %= 5
    routine.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:routine_list', pk=request.user.id)


@login_required
def routine_after(request, pk):
    routine = Routine.objects.get(id=pk)
    routine.period += 1
    routine.period %= 5
    routine.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('task:routine_list', pk=request.user.id)


@login_required
def change_routine_setting(request, pk):
    if request.user.pk != pk:
        return redirect('account_login')
    if not len(AddRoutine.objects.filter(user=request.user)):
        addroutine = AddRoutine(user=request.user, last_visited=datetime.date.today()-datetime.timedelta(days=1))
        addroutine.save()
    addroutine = AddRoutine.objects.get(user=request.user)
    addroutine.add_or_not ^= 1
    addroutine.save()
    return redirect('task:routine_list', pk=request.user.id)


# 完了タスク関連の操作
@login_required
def done(request, pk):
    task = Task.objects.get(id=pk)
    # task.done_or_not = True
    task.done_date = datetime.date.today()
    task.save()
    redirect_url = reverse('task:done_update', kwargs={'pk': pk})
    parameters = urlencode({'next': request.GET.get('next')})
    return redirect(f'{redirect_url}?{parameters}')

# @method_decorator(login_required, name='dispatch')
# class DoneView(UpdateView):
#   model = Task
#   form_class = DoneForm
#   template_name = 'task/done_update.html'

#   def form_valid(self, form):
#     return super(DoneView, self).form_valid(form)

#   def get_success_url(self):
#     return reverse_lazy('task:done_list', kwargs={'pk': self.request.user.id})


@method_decorator(login_required, name='dispatch')
class DoneUpdateView(UpdateView):
    model = Task
    form_class = DoneForm
    template_name = 'task/done_update.html'

    def form_valid(self, form):
        form.instance.done_or_not = True
        return super(DoneUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return reverse_lazy('task:done_list', kwargs={'pk': self.request.user.id})


@method_decorator(login_required, name='dispatch')
class DoneCreateView(CreateView):
    model = Task
    form_class = DoneForm
    template_name = 'task/done_create.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.done_or_not = True
        return super(DoneCreateView, self).form_valid(form)

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
    return redirect('top', pk=request.user.id)


def redirect_to_origin(request):
    redirect_to = request.GET.get('next')
    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=request.is_secure(),
    )
    if url_is_safe and redirect_to:
        return redirect(redirect_to)


def original_url(self):
    url = self.request.GET.get('next')
    url_is_safe = url_has_allowed_host_and_scheme(
        url=url,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=self.request.is_secure(),
    )
    if url_is_safe and url:
        return url
