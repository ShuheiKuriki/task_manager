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
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('form', views.form, name='form'),
    path('post', views.post),
    path('delete', views.delete),
    path('done', views.done),
    path('done_view', views.done_view),
    path('done_edit', views.done_edit),
    path('done_edit_view', views.done_edit_view),
    path('edit', views.edit),
    path('edit_view', views.edit_view),
    path('recover', views.recover),
    path('today', views.today),
    path('login_view', views.login_view, name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_user_view/', views.create_user_view),
    path('logout/',views.logout_view),
    path('accounts/login/', LoginView.as_view(template_name='login_view.html')),
]
