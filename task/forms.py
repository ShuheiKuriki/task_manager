from django.forms import ModelForm
from django import forms
from taskManager.models import Task
# from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(ModelForm):
    # deadline = forms.DateField(input_formats = '%m/%d/%Y')
    # when = forms.DateField(input_formats = '%m/%d/%Y')
    class Meta:
        model = Task
        fields = ['name','when','period','deadline','important','urgent']
        forms.CheckboxInput(attrs={'class': 'check'})
        widgets = {
            'deadline': DateInput(),
            'when': DateInput(),
            # 'important': forms.CheckboxInput(),
            # 'urgent': forms.CheckboxInput()
        }
        input_formats= {
            'deadline': ['%d %B %Y'],
            'when': ['%d %B %Y']
        }

class DoneEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','done_date']
        widgets = {
            'done_date': DateInput()
        }

# class EditForm(Form, task):
#     name = CharField('タスク名', max_length=256, default=task.name)
#     deadline = models.DateField('期限', default=task.deadline)
