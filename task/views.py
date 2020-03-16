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
from taskManager.views import Taskinfo

import datetime
# Create your views here.

# 未完了タスク関連の操作

# @method_decorator(login_required, name='dispatch')
# class TaskCreateView(CreateView):
#     form_class = TaskCreateForm
#     template_name = 'Form/create.html'
#
#     def form_valid(self, form):
#         form.instance.user_id = self.request.user.id
#         return super(TaskCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         try:
#             return original_url(self)
#         except:
#             return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

def create(request):
    if request.method == 'GET':
        form = TaskCreateForm()
        return render(request, 'task/create.html', {'form': form})
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
        try:
            return redirect_to_origin(request)
        except:
            return redirect('accounts:index', pk=request.user.id)

@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task/update.html'

    def get_success_url(self):
        try:
            return original_url(self)
        except:
            return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task/delete.html'

    def get_success_url(self):
        try:
            return original_url(self)
        except:
            return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

@login_required
def later(request, pk):
    task = Task.objects.get(id=pk)
    task.when += datetime.timedelta(days=1)
    task.save()
    return redirect('accounts:index', pk=request.user.id)

@login_required
def period_before(request, pk):
    task = Task.objects.get(id=pk)
    if task.period > 0:
        task.period -= 1
    task.save()
    try:
        return redirect_to_origin(request)
    except:
        return redirect('accounts:today', pk=request.user.id)

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
        return redirect('accounts:today', pk=request.user.id)

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
    return redirect('accounts:done_list', pk=request.user.id)

@method_decorator(login_required, name='dispatch')
class DoneUpdateView(UpdateView):
    model = Task
    form_class = DoneEditForm
    template_name = 'task/done_update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:done_list', kwargs={'pk': self.request.user.id})

@login_required
def done_before(request, pk):
    task = Task.objects.get(id=pk)
    task.done_date -= datetime.timedelta(days=1)
    task.save()
    return redirect('accounts:done_list', pk=request.user.id)

@login_required
def done_after(request, pk):
    task = Task.objects.get(id=pk)
    task.done_date += datetime.timedelta(days=1)
    task.save()
    return redirect('accounts:done_list', pk=request.user.id)

@login_required
def recover(request, pk):
    task = Task.objects.get(id=pk)
    task.done_or_not = False
    task.save()
    return redirect('accounts:index', pk=request.user.id)

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