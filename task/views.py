from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from .forms import TaskForm, DoneEditForm
from taskManager.models import Task
from taskManager.views import Taskinfo

import datetime
# Create your views here.

# 未完了タスク関連の操作
@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = 'Form/create.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'Form/update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'Form/delete.html'

    def get_success_url(self):
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
    template_name = 'Form/done_update.html'

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

