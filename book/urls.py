from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
  path('<int:pk>', views.index, name='index'),
  path('sort', views.sort, name='sort'),
  path('create', views.BookCreateView.as_view(), name='create'),
  path('<int:pk>/update', views.BookUpdateView.as_view(), name='update'),
  path('<int:pk>/delete', views.delete, name='delete'),
  path('<int:pk>/read', views.read, name='read'),
  path('<int:pk>/later', views.later, name='later'),
]