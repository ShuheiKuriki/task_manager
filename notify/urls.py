from django.urls import path
from . import views

app_name = 'notify'

urlpatterns = [
# LINE関連
path('callback/', views.callback, name='callback'),
path('notice',views.UpdateListView.as_view(), name='notice'),
path('line/', views.line, name='line'),
path('send/<str:when>', views.send, name='send'),
path('test', views.test)
]