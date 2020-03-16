from django.shortcuts import render

# 全ユーザー共通のページを表示
def index(request):
    return render(request, 'menu/index.html')

def sample(request):
    return render(request, 'menu/index_sample.html')

def notice(request):
    return render(request, 'menu/notice.html')

