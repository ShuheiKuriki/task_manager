from django.urls import path
from . import views

app_name = 'shoppinglist'

urlpatterns = [
    path('<int:pk>', views.index, name='index'),
    path('set_default', views.set_default, name='set_default'),
    path('buy/<int:pk>', views.buy, name='buy'),
    path('must_buy/<int:pk>', views.must_buy, name='must_buy'),
    path('not_buy/<int:pk>', views.not_buy, name='not_buy'),
    path('create', views.ShoppingCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.ShoppingUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
]