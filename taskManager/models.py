from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Task(models.Model):
    periods = ['~12時','12~15時','15~18時','18~21時','21時~']
    choices=[(i,period) for i,period in enumerate(periods)]

    name = models.CharField('タスク名', max_length=256, blank=True)
    deadline = models.DateField('期限', default=now, blank=True, null=True)
    important = models.BooleanField('重要', default=False)
    expired = models.BooleanField('期限切れ', default=False)
    urgent = models.BooleanField('緊急', default=False)
    when = models.DateField('実行予定日', default=now, blank=True)
    period = models.IntegerField('時間帯', choices=choices, default=0)

    done_or_not = models.BooleanField(default=False)
    done_date = models.DateField('完了した日', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField('順番', default=0)

    def __str__(self):
        return self.name

    def get_list(self):
        important = '○' if self.important == True else '×'
        urgent = '○' if self.urgent == True else '×'
        return {'タスク名':self.name, '実行予定日':self.when, '時間帯':self.periods[self.period],
                '期限':self.deadline, '重要': important, '緊急':urgent}


class LinePush(models.Model):
    line_id = models.CharField('ユーザーID', max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)



# class Done(models.Model):
#     name = models.CharField(max_length=256)
#     id = models.AutoField(primary_key=True)
