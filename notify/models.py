from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.template.loader import render_to_string
from linebot import LineBotApi
from linebot.models import TextSendMessage
from taskManager.models import LinePush
import logging, os

logger = logging.getLogger(__name__)

# Create your models here.

class Update(models.Model):
    # test = models.CharField('テスト', default='test', max_length=255)

    title = models.CharField('機能名', default='',max_length=255, blank=True)
    description = models.TextField('機能追加の説明', default='', blank=True)
    updated_at = models.DateField('追加日', default=now, blank=True)
    updated_or_not = models.BooleanField('更新済み', default=False)

    def __str__(self):
        return self.title

    def line_push(self, request):
        """記事をラインで通知"""
        context = {
            'update': self,
        }
        message = render_to_string('notify/message/notify_update.txt', context, request)
        try:
            CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
        except:
            CHANNEL_ACCESS_TOKEN = getattr(settings, "CHANNEL_ACCESS_TOKEN", None)
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        for push in LinePush.objects.all():
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
