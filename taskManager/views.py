from django.shortcuts import render

class Taskinfo:
    def __init__(self, tasks, name=""):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        n = int((self.num*2)**(1/2))
        if n*(n+1)/2 <= self.num:
            self.level = n
        else:
            self.level = n-1

# 全ユーザー共通のページを表示
def index(request):
    return render(request, 'menu/index.html')

def sample(request):
    return render(request, 'menu/index_sample.html')

def notice(request):
    return render(request, 'menu/notice.html')

