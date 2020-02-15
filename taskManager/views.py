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
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os
import logging

logger = logging.getLogger(__name__)
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

class Taskinfo:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        self.level = (self.num-1)//10+1


def list(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    today = Taskinfo(
        name="今日",
        tasks=tasks.filter(when__lte=datetime.date.today()).order_by('order')
    )
    tom = Taskinfo(
        name="明日",
        tasks=tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
    )
    other = Taskinfo(
        name="明日以降",
        tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when')
    )
    infos = [today, tom, other]
    return render(request, 'list.html', {'infos':infos})

def form(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    form = TaskForm()
    return render(request, 'form.html', {'form': form})

def done_view(request,pk):
    if request.user.pk != pk:
        return redirect('login')
    dones = Task.objects.all().filter(user=request.user, done_or_not=True).order_by('-done_date')
    infos = []
    names = ["今日", "昨日", "一昨日", "3日前", "4日前", "5日前", "6日前"]
    total = 0
    for i in range(7):
        info = Taskinfo(
            name = names[i],
            tasks = dones.filter(done_date=datetime.date.today()-datetime.timedelta(days=i))
        )
        total += info.num
        infos.append(info)
    total_level = (total-1)//10+1
    today = infos[0].num
    return render(request, 'done.html', {'infos':infos, 'today':today, 'total':total,'level':total_level})

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
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
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

@login_required
def line(request):
    return render(request, 'add_line.html')

@csrf_exempt
def callback(request):
    """ラインの友達追加時に呼び出され、ラインのIDを登録する。"""
    # logger.error('OK')
    CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
    # except:
        # CHANNEL_SECRET = "bab444d6e36c50020cd500a0cacdfb08"
    logger.error("OK")
    # logger.error(CHANNEL_SECRET)
    handler = WebhookHandler(CHANNEL_SECRET)
    # logger.error(handler)
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    # logger.error(signature)
    # リクエストボディを取得
    # body = request.body.decode('utf-8')
    # logger.error(body)
    # try:
    #     # 署名の検証を行い、成功した場合にhandleされたメソッドを呼び出す
    #     handler.handle(body, signature)
    #     logger.error("OK")
    # except:
    #     # 署名検証で失敗したときは例外をあげる
    #     logger.error("fail")
    #     return HttpResponseForbidden()
    # handleの処理を終えればOK
    # return HttpResponse('OK')
    if request.method == 'POST':
        logger.error('POST')
    #     pass
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        # logger.error(events)
        line_user_id = events[0]['source']['userId']
        # # チャネル設定のWeb hook接続確認時にはここ。このIDで見に来る。
        logger.error(line_user_id)
        if line_user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
            pass
        # 友達追加時・ブロック解除時
        elif events[0]['type'] == 'follow':
            logger.error("follow")
            linepush = LinePush.objects.create(line_id=line_user_id)
            linepush.save()
            logger.error("追加しました")
        # アカウントがブロックされたとき
        elif events[0]['type'] == 'unfollow':
            logger.error("unfollow")
            LinePush.objects.filter(line_id=line_user_id).delete()
    return HttpResponse()
    # return render(request, 'notify_message.txt', {'request':request})

def test(request):
    return HttpResponse(Task.objects.all().get(id=1).name)

def notify(request, when):
    CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    users = LinePush.objects.all()
    logger.error(len(users))
    if len(users) == 0:
        return HttpResponse("送信する相手がいません")
    else:
        for push in users:
            logger.error(when)
            tasks_today = Task.objects.all().filter(user=push.user, done_or_not=False, when__lte=datetime.date.today()).order_by('order')
            tasks_tom = Task.objects.all().filter(user=push.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
            context = {
                'tasks': {"today" : tasks_today, "tom": tasks_tom},
                "id" : push.user.id
            }
            if when == 'night':
                text = "notify_message_night.txt"
            else:
                text = "notify_message.txt"
            message = render_to_string(text, context, request)
            logger.error("message ready")
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
        return HttpResponse("送信しました")
