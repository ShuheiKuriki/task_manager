# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.conf import settings

from .forms import ShoppingForm, SortForm
from .models import Shopping

import datetime
from datetime import date

# Create your views here.

def set_default(request):
    shoppings = Shopping.objects.filter(user=request.user, buy_date=None)
    for shopping in shoppings:
        shopping.buy_date = date.today()
        shopping.save()
    return HttpResponse('OK')

def buy(request,pk):
    shopping = Shopping.objects.get(id=pk)
    shopping.buy_or_not = True
    shopping.date = date.today()
    shopping.save()
    return redirect('shoppinglist:index', pk=request.user.id)

def must_buy(request,pk):
    shopping = Shopping.objects.get(id=pk)
    shopping.buy_or_not = False
    shopping.save()
    return redirect('shoppinglist:index', pk=request.user.id)

def not_buy(request,pk):
    shopping = Shopping.objects.get(id=pk)
    shopping.buy_or_not = True
    shopping.save()
    return redirect('shoppinglist:index', pk=request.user.id)

class Shoppinginfo:
    def __init__(self, shoppings, name="",day=''):
        self.name = name
        self.shoppings = shoppings
        self.num = len(shoppings)
        if day=='':
            self.date=''
        else:
            day_delta = date.today()+datetime.timedelta(days=day)
            week_day = ['月','火','水','木','金','土','日']
            self.date = "{}/{}({})".format(day_delta.month, day_delta.day, week_day[day_delta.weekday()])
        S = 0
        for shopping in shoppings:
            if shopping.price is not None:
                S += shopping.price * shopping.count
            if shopping.date is not None:
                shopping.days = (date.today() - shopping.date).days
            shopping.save()
        self.total = S

def index(request,pk):
    if request.user.pk != pk:
        return redirect('account_login')
    shoppings = Shopping.objects.filter(user=request.user)
    past_shoppings = shoppings.filter(buy_date__lt=date.today())
    for past_shopping in past_shoppings:
        past_shopping.buy_date = date.today()
        past_shopping.save()
    not_buy = shoppings.filter(buy_or_not=False)
    today = Shoppinginfo(name="今日", day=0,
            shoppings=not_buy.filter(buy_date=date.today()).order_by('shop'))
    tom = Shoppinginfo(name="明日", day=1,
            shoppings=not_buy.filter(buy_date=date.today()+datetime.timedelta(days=1)).order_by('shop'))
    infos = [today, tom]
    for i in range(2,8):
        infos.append(Shoppinginfo(day=i,
            shoppings=not_buy.filter(buy_date=date.today()+datetime.timedelta(days=i)).order_by('shop')))
    bought = Shoppinginfo(name="過去に購入した商品",
            shoppings=shoppings.filter(buy_or_not=True).order_by('-date'))
    return render(request, 'shoppinglist/shopping_list.html', {'infos':infos,'bought':bought})

@method_decorator(login_required, name='dispatch')
class ShoppingCreateView(CreateView):
    form_class = ShoppingForm
    template_name = 'shoppinglist/shopping_create.html'

    def get_success_url(self):
        return reverse_lazy('shoppinglist:index',kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(ShoppingCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class ShoppingUpdateView(UpdateView):
    model = Shopping
    form_class = ShoppingForm

    def get_success_url(self):
        return reverse_lazy('shoppinglist:index',kwargs={'pk': self.request.user.id})

@require_POST
def delete(request,pk):
    shopping = get_object_or_404(Shopping, pk=pk)
    shopping.delete()
    return redirect('shoppinglist:index', pk=request.user.id)