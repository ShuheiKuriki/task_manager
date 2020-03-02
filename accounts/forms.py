from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    #ログオンフォームの定義
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields.values():
            fields.widget.attrs['class'] = 'form-control'
            fields.widget.attrs['placeholder']= fields.label