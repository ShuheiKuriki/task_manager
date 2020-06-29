if 'import':
    from django.shortcuts import render, redirect, get_object_or_404
    from django.http import HttpResponse
    from django.contrib.auth.decorators import login_required
    from django.urls import reverse_lazy,reverse
    from django.utils.decorators import method_decorator
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_POST
    from django.utils.http import is_safe_url
    from django.views.generic import CreateView, UpdateView, DeleteView
    from django.conf import settings

    from urllib.parse import urlencode
    from .forms import TaskCreateForm, TaskUpdateForm, DoneForm
    from taskManager.models import Task

    import datetime
    from datetime import date
# Create your views here.
class Taskinfo:
    def __init__(self, tasks, name="", day=''):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        if day=='':
            self.date=''
        else:
            day_delta = date.today()+datetime.timedelta(days=day)
            week_day = ['月', '火', '水','木','金','土','日']
            self.date = "{}/{}({})".format(day_delta.month, day_delta.day, week_day[day_delta.weekday()])
        n = int((self.num*2)**(1/2))
        if n*(n+1)/2 <= self.num:
            self.level = n
        else:
            self.level = n-1

def list(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    todays = tasks.filter(when__lte=datetime.date.today())
    for task in todays:
        task.when = date.today()
        task.save()
    for task in todays:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    today_num = len(todays)
    names = ['~12時','12~15時','15~18時','18~21時','21時~']
    h = datetime.datetime.now().hour
    p = max(h//3-3,0)
    today_infos = []
    for i,name in enumerate(names):
        if i<p:
            continue
        elif i==p:
            info = Taskinfo(name=name, tasks=todays.filter(period__lte=i).order_by('order'))
        else:
            info = Taskinfo(name=name, tasks=todays.filter(period=i).order_by('order'))
        if info.num>0:
            today_infos.append(info)
    toms = tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1))
    for task in toms:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    tom_num = len(toms)
    tom_infos = []
    for i,name in enumerate(names):
        info = Taskinfo(name=name, tasks=toms.filter(period=i).order_by('order'))
        if info.num>0:
            tom_infos.append(info)
    other = Taskinfo(name="明日以降",tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when'))
    return render(request, 'task/list.html', {'today_infos':today_infos, 'today_num':today_num, 'tom_infos':tom_infos, 'tom_num':tom_num, 'other':other})
    
def done_list(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    week = Taskinfo(tasks = dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7)))
    data = []
    for i in range(6,-1,-1):
        dat = date.today()-datetime.timedelta(days=i)
        info = Taskinfo(tasks = dones.filter(done_date=dat))
        data.append(info.num)
    return render(request, 'task/done_list.html', {'week':week, 'today':data[-1],'data':data})

#未完了タスク関連
def create(request):
    if request.method == 'GET':
        form = TaskCreateForm()
        nex = request.GET.get('next')
        return render(request, 'task/task_create.html', {'form': form,'next': nex})
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
    template_name = 'task/task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return original_url(self)

@require_POST
def delete(request,pk):
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
        p = max(h//3-3,0)
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
    for order, id in enumerate(request.POST.getlist('task[]')):
        print(order,id)
        task = Task.objects.get(id=id)
        task.order = order
        task.save()
    return HttpResponse('')

# 完了タスク関連の操作

@login_required
def done(request, pk):
    task = Task.objects.get(id=pk)
    # task.done_or_not = True
    task.done_date = datetime.date.today()
    task.save()
    redirect_url = reverse('task:done_update', kwargs={'pk':pk})
    parameters = urlencode({'next':request.GET.get('next')})
    return redirect(f'{redirect_url}?{parameters}')

# @method_decorator(login_required, name='dispatch')
# class DoneView(UpdateView):
    #     model = Task
    #     form_class = DoneForm
    #     template_name = 'task/done_update.html'

    #     def form_valid(self, form):
    #         return super(DoneView, self).form_valid(form)

    #     def get_success_url(self):
    #         return reverse_lazy('task:done_list', kwargs={'pk': self.request.user.id})

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