from django.forms import ModelForm
from django import forms
from .models import Book
# from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','genre','deadline']
        forms.CheckboxInput(attrs={'class': 'check'})
        widgets = {
            'deadline': DateInput(),
        }

