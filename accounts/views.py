# Create your views here.
from django.shortcuts import redirect

def profile(request):
    return redirect('top', pk=request.user.id)
