from django.forms import Form, CharField, ModelForm
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']

class TaskForm(Form):
    タスク名 = CharField(max_length=256)
