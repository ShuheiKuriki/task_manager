from django.shortcuts import render
from django.views.generic import TemplateView
from book.views import Bookinfo
from book.models import Book
from taskManager.models import Task
import datetime
from datetime import date

class Taskinfo:
    def __init__(self, tasks, name="", day=''):
        self.name = name
        self.tasks = tasks[:3]
        self.num = len(tasks)

class IndexView(TemplateView):
    template_name = 'menu/index.html'

class IndexSampleView(TemplateView):
    template_name = 'menu/index_sample.html'

def top(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    tasks = Task.objects.all().filter(user=request.user, done_or_not=False)
    past_tasks = tasks.filter(when__lt=datetime.date.today())
    for past_task in past_tasks:
        past_task.when = datetime.date.today()
        past_task.save()
    for task in tasks:
        task.expired = True if task.deadline<datetime.date.today() else False
        task.save()
    today = Taskinfo(name="今日", day=0,
        tasks=tasks.filter(when=datetime.date.today()).order_by('deadline'))
    tom = Taskinfo(name="明日", day=1,
        tasks=tasks.filter(when=datetime.date.today()+datetime.timedelta(days=1)).order_by('deadline'))
    other = Taskinfo(name="明日以降",
        tasks=tasks.filter(when__gt=datetime.date.today()+datetime.timedelta(days=1)).order_by('when'))
    task_infos = [today, tom, other]
    books = Book.objects.all().filter(user=request.user, done_or_not = False)
    for book in books:
        book.expired = True if book.deadline<date.today() else False
        book.save()
    book_infos = []
    genres = ["アカデミック","テクノロジー","ビジネス","自己啓発","小説"]
    for genre in genres:
        book_info = Bookinfo(name=genre, books=books.filter(genre=genre).order_by('order'))
        book_infos.append(book_info)
    return render(request, 'menu/top.html', {'task_infos':task_infos, 'book_infos':book_infos})