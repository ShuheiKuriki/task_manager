from django.db import models
from django.utils import timezone

class Task(models.Model):
    name = models.CharField('タスク名', max_length=256, blank=True)
    id = models.AutoField(primary_key=True)
    deadline = models.DateField('期限', default=timezone.now, blank=True)
    when = models.DateField('実行予定日', default=timezone.now, blank=True)
    done_or_not = models.BooleanField(default=False)

# class Done(models.Model):
#     name = models.CharField(max_length=256)
#     id = models.AutoField(primary_key=True)
