from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.profile),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('', views.index, name='index'),
]