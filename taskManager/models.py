from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField('タスク名', max_length=256, blank=True)
    # id = models.AutoField(primary_key=True)
    deadline = models.DateField('期限', default=now, blank=True, null=True)
    important = models.BooleanField('重要')
    urgent = models.BooleanField('緊急')
    when = models.DateField('実行予定日', default=now, blank=True)
    period = models.IntegerField('時間帯', default=0)
    done_or_not = models.BooleanField(default=False)
    done_date = models.DateField('完了した日', default=now, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField('順番', default=0)

    def __str__(self):
        return self.name

class LinePush(models.Model):
    line_id = models.CharField('ユーザーID', max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user



# class Done(models.Model):
#     name = models.CharField(max_length=256)
#     id = models.AutoField(primary_key=True)
