from django.shortcuts import render

class Taskinfo:
    def __init__(self, tasks, name=""):
        self.name = name
        self.tasks = tasks
        self.num = len(tasks)
        self.level = (self.num-1)//10+1

# 全ユーザー共通のページを表示
def index(request):
    return render(request, 'Menu/index.html')

def sample(request):
    return render(request, 'Menu/index_sample.html')

def notice(request):
    return render(request, 'Menu/notice.html')