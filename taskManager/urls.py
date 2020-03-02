"""taskManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('allauth.urls')),     # 追加

    # 全ユーザー共通のページを表示
    path('', views.index, name='index'),
    path('sample', views.sample),
    path('notice', views.notice, name='notice'),

    # ユーザーに固有の一覧ページ
    # path('<int:pk>', views.list, name='list'),
    # path('<int:pk>/today', views.today, name='today'),
    # path('<int:pk>/tomorrow', views.tomorrow, name='tomorrow'),
    # path('<int:pk>/done_list', views.done_list, name='done_list'),

    # 未完了タスク関連の操作
    path('create', views.TaskCreateView.as_view()),
    path('update/<int:pk>', views.TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.TaskDeleteView.as_view(), name='delete'),
    path('later/<int:pk>', views.later, name='later'),
    path('sort', views.sort, name='sort'),

    # 完了タスク関連の操作
    path('done/<int:pk>', views.done, name='done'),
    path('done_update/<int:pk>', views.DoneUpdateView.as_view(), name='done_update'),
    path('recover/<int:pk>', views.recover, name='recover'),

    # LINE関連
    path('callback/', views.callback, name='callback'),
    path('line/', views.line, name='line'),
    path('notify/<str:when>', views.notify, name='notify'),
    path('test', views.test)
]

# if settings.DEBUG:    # この if 文 (5STEP) を追加します。
import debug_toolbar
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
