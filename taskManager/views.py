from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import render_to_string
from .forms import TaskForm, UserForm, DoneEditForm
from .models import Task, LinePush
import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import linebot
from linebot.models import TextSendMessage

def index(request):
    return render(request, 'index.html')

def sample(request):
    return render(request, 'index_sample.html')

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
    user = UserForm(request.POST)
    if user.is_valid():
        user=User.objects.create_user(
        request.POST.get('username'),
        request.POST.get('email'),
        request.POST.get('password')
    )
        user.save()
        return redirect('/accounts/login/')
    else:
        return redirect('/create_user_view')

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
            important=form.cleaned_data['important'],
            urgent=form.cleaned_data['urgent'],
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
            task.important = request.POST['important']
            task.urgent = request.POST['urgent']
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
    tasks_today = tasks.filter(when__lte=datetime.date.today()).order_by('order')
    tasks_tom = tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
    tasks = tasks.filter(user=request.user, done_or_not=False, when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when')
    num_today = len(tasks_today)
    num_tom = len(tasks_tom)
    num = len(tasks)
    today = {'tasks':tasks_today, 'num':num_today, 'name':'今日'}
    tom = {'tasks':tasks_tom, 'num':num_tom, 'name':'明日'}
    other = {'tasks':tasks, 'num':num, 'name':'明日以降'}
    dics = [today, tom, other]
    return render(request, 'list.html', {'dics':dics})

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
    num = len(dones)
    today = {'done':done_today, 'num':num_today, 'name':'今日'}
    yes = {'done':done_yes, 'num':num_yes, 'name':'昨日'}
    other = {'done':dones, 'num':num, 'name':'昨日以前'}
    dics = [today, yes, other]
    if num_today == 0:
        message = '昨日は{}個のタスクをこなしました。今日も頑張りましょう！'.format(num_yes)
    else:
        message = '今日は{}個のタスクをこなしました。よく頑張りましたね！'.format(num_today)
    return render(request, 'done.html', {'dics':dics, 'message':message})

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
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when__lte=datetime.date.today()).order_by('order')
    num = len(tasks)
    return render(request, 'today.html', {'tasks':tasks,'num':num})

def tomorrow(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1)).order_by('deadline')
    num = len(tasks)
    return render(request, 'tomorrow.html', {'tasks':tasks,'num':num})

def notice(request):
    return render(request, 'notice.html')

@csrf_exempt
def sort(request):
    for order, id in enumerate(request.POST.getlist('task[]')):
        task = Task.objects.get(id=id)
        task.order = order
        task.save()
    return HttpResponse('')

@csrf_exempt
def callback(request):
    """ラインの友達追加時に呼び出され、ラインのIDを登録する。"""
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_user_id = events[0]['source']['userId']
        # チャネル設定のWeb hook接続確認時にはここ。このIDで見に来る。
        if line_user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
            return HttpResponse("接続確認されました")
        # 友達追加時・ブロック解除時
        elif events[0]['type'] == 'follow':
            LinePush.objects.create(user_id=line_user_id)
            return HttpResponse("登録しました")
        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            LinePush.objects.filter(user_id=line_user_id).delete()
            return HttpResponse("登録解除しました")

    return HttpResponse("登録していません")

def notify(request):
    line_bot_api = linebot.LineBotApi('ffezaFUdv0+TQl/LDJ15LziQLKiekNyl5qwkMyLDtPXFZ2b97w9ZR+qZSIuZ6OSrbcWa2J0sVJDttSoUE8alOPWeh4R8zW/mh3s1emX6v6XlVKz5hvgpCi5YQ0vNbHwDCVHAaWNcpszacPzgIvvuggdB04t89/1O/w1cDnyilFU=')
    users = LinePush.objects.all()
    if len(users) == 0:
        return HttpResponse("送信する相手がいません")
    else:
        for push in LinePush.objects.all():
            context = {
                'task': "散歩する",
            }
            message = render_to_string('notify_message.txt', context, request)
            line_bot_api.push_message(push.user_id, messages=TextSendMessage(text=message))
        return HttpResponse("送信しました")
