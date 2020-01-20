from django.forms import Form, CharField, DateTimeField, ModelForm
from django.contrib.auth.models import User
from .models import Task
# from django.utils import timezone

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('done_date',)

# class EditForm(Form, task):
#     name = CharField('タスク名', max_length=256, default=task.name)
#     deadline = models.DateField('期限', default=task.deadline)
