from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
path('redirect', views.redirect_to_origin, name='redirect'),
#リスト
path('<int:pk>/list', views.list, name='list'),
path('<int:pk>/done_list', views.done_list, name='done_list'),

# 未完了タスク関連の操作
path('create', views.create, name='create'),
path('<int:pk>/update', views.TaskUpdateView.as_view(), name='update'),
path('<int:pk>/delete', views.delete, name='delete'),
path('<int:pk>/later', views.later, name='later'),
path('<int:pk>/period_before', views.period_before, name='period_before'),
path('<int:pk>/period_after', views.period_after, name='period_after'),
path('sort', views.sort, name='sort'),

# 完了タスク関連の操作
path('<int:pk>/done', views.DoneView.as_view(), name='done'),
path('<int:pk>/done_before', views.done_before, name='done_before'),
path('<int:pk>/done_after', views.done_after, name='done_after'),
path('<int:pk>/done_update', views.DoneUpdateView.as_view(), name='done_update'),
path('done_create', views.DoneCreateView.as_view(), name='done_create'),
path('<int:pk>/recover', views.recover, name='recover'),
]