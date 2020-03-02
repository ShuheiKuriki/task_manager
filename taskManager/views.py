from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from .forms import TaskForm, UserForm, DoneEditForm
from .models import Task, LinePush

import datetime
import json
import os
import logging

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

logger = logging.getLogger(__name__)

class Taskinfo:
    def __init__(self, tasks, name=""):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        self.level = (self.num-1)//10+1

# 全ユーザー共通のページを表示
def index(request):
    return render(request, 'index.html')

def sample(request):
    return render(request, 'index_sample.html')

def notice(request):
    return render(request, 'Menu/notice.html')

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
    return redirect(to='/accounts/'+str(request.user.id))

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
    return redirect(to='/accounts/'+str(request.user.id)+'/done_list')

@method_decorator(login_required, name='dispatch')
class DoneUpdateView(UpdateView):
    model = Task
    form_class = DoneEditForm
    template_name = 'Form/done_update.html'

    def get_success_url(self):
        return reverse_lazy('accounts:done_list', kwargs={'pk': self.request.user.id})

@login_required
def recover(request, pk):
    task = Task.objects.get(id=pk)
    task.done_or_not = False
    task.save()
    return redirect('/accounts/'+str(request.user.id))


# ユーザー情報関連
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

class MyLoginView(LoginView):
    template_name = 'Form/login.html'

    def get_success_url(self):
        # return reverse('index')
        return reverse_lazy('accounts:index', kwargs={'pk': self.request.user.id})

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'Form/create_user.html'
    success_url = reverse_lazy('accounts:login')

# LINE関連
@login_required
def line(request):
    return render(request, 'Menu/add_line.html')

@csrf_exempt
def callback(request):
    """ラインの友達追加時に呼び出され、ラインのIDを登録する。"""
    # logger.error('OK')
    try:
        CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
    except:
        CHANNEL_SECRET = getattr(settings, "CHANNEL_SECRET", None)

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
    try:
        CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
    except:
        CHANNEL_ACCESS_TOKEN = getattr(settings, "CHANNEL_ACCESS_TOKEN", None)

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    users = LinePush.objects.all()
    logger.error(len(users))
    if len(users) == 0:
        return HttpResponse("送信する相手がいません")
    else:
        for push in users:
            logger.error(when)
            today = Taskinfo(
                    name = "今日",
                    tasks = Task.objects.all().filter(user=push.user, done_or_not=False, when__lte=datetime.date.today()).order_by('order')
            )
            tom = Taskinfo(
                    name = "明日",
                    tasks = Task.objects.all().filter(user=push.user, done_or_not=False, when=datetime.date.today()+datetime.timedelta(days=1)).order_by('order')
            )
            context = {
                'today': today,
                'tom': tom,
                "id" : push.user.id
            }
            logger.error(context)
            if when == 'report':
                text = "notify_report.txt"
                dones = Task.objects.all().filter(user=push.user, done_or_not=True).order_by('-done_date')
                done_today = Taskinfo(
                        tasks = dones.filter(done_date=datetime.date.today())
                )
                done_week = Taskinfo(
                        tasks = dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7))
                )
                context["done_today"]=done_today
                context["done_week"]=done_week
            else:
                text = "notify_message.txt"
            message = render_to_string(text, context, request)
            logger.error("message ready")
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
        return HttpResponse("送信しました")
