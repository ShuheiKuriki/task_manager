from django.forms import Form, CharField

class TaskForm(Form):
    タスク名 = CharField(max_length=256)
