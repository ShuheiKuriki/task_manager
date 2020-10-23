from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import django

class Routine(models.Model):
  periods = ['~12時','12~15時','15~18時','18~21時','21時~']
  period_choice=[(i,period) for i,period in enumerate(periods)]
  day_types = ['毎日', '月', '火', '水', '木', '金', '土', '日']
  day_choice=[(i,day_type) for i,day_type in enumerate(day_types)]
  
  name = models.CharField('ルーティン名', max_length=256, blank=True)
  important = models.BooleanField('重要', default=False)
  urgent = models.BooleanField('緊急', default=False)
  period = models.IntegerField('時間帯', choices=period_choice, default=0)
  days = models.IntegerField('曜日タイプ', choices=day_choice, default=0)

  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_list(self):
    important = '○' if self.important == True else '×'
    urgent = '○' if self.urgent == True else '×'
    return {'ルーティン名':self.name, '時間帯':self.periods[self.period],
        '期限':self.deadline, '重要': important, '緊急':urgent}

class AddRoutine(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  last_visited = models.DateField(default=now)
  add_or_not = models.BooleanField(default=False)
