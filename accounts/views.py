# Create your views here.
from django.shortcuts import redirect

def profile(request):
    return redirect('task:list', pk=request.user.id)
