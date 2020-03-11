from django.forms import ModelForm
from django import forms
from taskManager.models import Task
# from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskCreateForm(ModelForm):
    # deadline = forms.DateField(input_formats = '%m/%d/%Y')
    # when = forms.DateField(input_formats = '%m/%d/%Y')
    rep_type = [('0', 'なし'),('1', '毎日'),('7', '毎週'),('14', '2週間ごと')]
    repeat =  forms.ChoiceField(label='繰り返し', choices=rep_type)
    num =  forms.ChoiceField(label='繰り返し回数', choices=[(str(i),str(i)) for i in range(1,11)])
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
class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','when','period','deadline','important','urgent']
        forms.CheckboxInput(attrs={'class': 'check'})
        widgets = {
            'deadline': DateInput(),
            'when': DateInput(),
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
