from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=256)
    id = models.AutoField(primary_key=True)

class Done(models.Model):
    name = models.CharField(max_length=256)
    id = models.AutoField(primary_key=True)
