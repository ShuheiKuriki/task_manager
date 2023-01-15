from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.generic import ListView
from taskManager.models import Task, LinePush
from task.views import Taskinfo

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

from .models import Update
import datetime, logging, json, os

logger = logging.getLogger(__name__)

# Create your views here.
# LINE関連
@login_required
def line(request):
    return render(request, 'menu/add_line.html')

class UpdateListView(ListView):
    model = Update
    template_name = 'notify/notice.html'

    def get_queryset(self):
        return Update.objects.all().order_by('-updated_at')

@csrf_exempt
def callback(request):
    """ラインの友達追加時に呼び出され、ラインのIDを登録する。"""
    # logger.error('OK')
    try:
        CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
    except:
        CHANNEL_SECRET = getattr(settings.dev, "CHANNEL_SECRET", None)

    logger.error("OK")
    # logger.error(CHANNEL_SECRET)
    # handler = WebhookHandler(CHANNEL_SECRET)
    # logger.error(handler)
    # リクエストヘッダーから署名検証のための値を取得
    # signature = request.META['HTTP_X_LINE_SIGNATURE']
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


def send(request, when):
    try:
        CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
    except:
        CHANNEL_ACCESS_TOKEN = getattr(settings, "CHANNEL_ACCESS_TOKEN", None)
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    users = LinePush.objects.all()
    print(len(users))
    if len(users) == 0:
        return HttpResponse("送信する相手がいません")
    else:
        for push in users:
            print(when)
            tasks = Task.objects.all().filter(user=push.user, done_or_not=False)
            todays = tasks.filter(when__lte=datetime.date.today())
            num = len(todays)
            names = ['~12時','12~15時','15~18時','18~21時','21時~']
            h = datetime.datetime.now().hour
            p = max(h//3-3,0)
            today_info = []
            for i,name in enumerate(names):
                if i<p:
                    continue
                elif i==p:
                    info = Taskinfo(name=name, tasks=todays.filter(period__lte=i).order_by('order'))
                else:
                    info = Taskinfo(name=name, tasks=todays.filter(period=i).order_by('order'))
                if info.num>0:
                    today_info.append(info)
            context = {'today': today_info, 'num':num}
            print(context)
            if when == 'report':
                text = "notify/message/notify_report.txt"
                tomorrow = tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1))
                tom_num = len(tomorrow)
                context["tom_num"]=tom_num
                tom_info = []
                for i,name in enumerate(names):
                    info = Taskinfo(name=name, tasks=tomorrow.filter(period=i).order_by('order'))
                    if info.num>0:
                        tom_info.append(info)
                context['tom_info']=tom_info
                dones = Task.objects.all().filter(user=push.user, done_or_not=True).order_by('-done_date')
                done_today = Taskinfo(tasks = dones.filter(done_date=datetime.date.today()))
                done_week = Taskinfo(tasks = dones.filter(done_date__gt=datetime.date.today()-datetime.timedelta(days=7)))
                context["done_today"]=done_today
                context["done_week"]=done_week
            else:
                text = "notify/message/notify_message.txt"
            message = render_to_string(text, context, request)
            print("message ready")
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
        return HttpResponse("送信しました")