from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .forms import BookForm
from .models import Book

import datetime
from datetime import date

class Bookinfo:
    def __init__(self, books, name=""):
        self.name = name
        self.books = books
        self.num = len(books)

def list(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    books = Book.objects.all().filter(user=request.user, done_or_not = False)
    for book in books:
        book.expired = True if book.deadline<date.today() else False
        book.save()
    infos = []
    genres = ["小説","アカデミック","ビジネス","自己啓発"]
    for genre in genres:
        info = Bookinfo(name=genre, books=books.filter(genre=genre).order_by('order'))
        infos.append(info)
    return render(request, 'book/book_list.html', {'infos':infos})

@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    form_class = BookForm
    template_name = 'book/book_create.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(BookCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book:list', kwargs={'pk': self.request.user.id})

@method_decorator(login_required, name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        return reverse_lazy('book:list', kwargs={'pk': self.request.user.id})

@require_POST
def delete(request,pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book:list',pk=request.user.id)

@csrf_exempt
def sort(request):
    for order, id in enumerate(request.POST.getlist('book[]')):
        book = Book.objects.get(id=id)
        book.order = order
        book.save()
    return HttpResponse('')

@login_required
def read(request, pk):
    book = Book.objects.get(id=pk)
    book.done_or_not = True
    book.done_date = date.today()
    book.save()
    return redirect('book:list', pk=request.user.id)

@login_required
def later(request, pk):
    book = Book.objects.get(id=pk)
    book.deadline += datetime.timedelta(days=1)
    book.save()
    return redirect('book:list', pk=request.user.id)