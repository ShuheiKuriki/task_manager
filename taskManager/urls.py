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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('notify/', include('notify.urls')),
    path('task/', include('task.urls')),
    path('book/', include('book.urls')),
    path('shoppinglist/', include('shoppinglist.urls')),
    # path('auth/', include('allauth.urls')),     # 追加

    # 全ユーザー共通のページを表示
    path('', views.IndexView.as_view(), name='index'),
    path('sample', views.IndexSampleView.as_view(), name='sample'),
    # トップページ
    path('<int:pk>/top', views.top, name='top'),
]

# if settings.DEBUG:    # この if 文 (5STEP) を追加します。
import debug_toolbar
urlpatterns += [
  path('__debug__/', include(debug_toolbar.urls))
  ]
