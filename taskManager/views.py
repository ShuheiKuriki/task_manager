from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def form(request):
    return render(request, 'form.html')
