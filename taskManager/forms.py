from django.forms import Form, CharField, ModelForm
from django import forms
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
        fields = ['name','when','deadline','important','urgent']
        # widgets = {
        #     'deadline': forms.SelectDateWidget,
        #     'when': forms.SelectDateWidget
        # }

class DoneEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['done_date']
        # widgets = {
        #     'done_date': forms.SelectDateWidget
        # }

# class EditForm(Form, task):
#     name = CharField('タスク名', max_length=256, default=task.name)
#     deadline = models.DateField('期限', default=task.deadline)
