from django.forms import Form, CharField

class TaskForm(Form):
    name = CharField(max_length=256)
