from django.db import models
import datetime

class Task(models.Model):
    name = models.CharField('タスク名', max_length=256, blank=True)
    id = models.AutoField(primary_key=True)
    deadline = models.DateField('期限', default=datetime.date.today(), blank=True, null=True)
    when = models.DateField('実行予定日', default=datetime.date.today(), blank=True)
    done_or_not = models.BooleanField(default=False)
    done_date = models.DateField('完了した日', default=datetime.date.today(), blank=True, null=True)


# class Done(models.Model):
#     name = models.CharField(max_length=256)
#     id = models.AutoField(primary_key=True)
