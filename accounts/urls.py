from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.profile),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('', views.index, name='index'),
    path('<int:pk>', views.index, name='index'),
    path('<int:pk>/today', views.today, name='today'),
    path('<int:pk>/tomorrow', views.tomorrow, name='tomorrow'),
    path('<int:pk>/done_list', views.done_list, name='done_list'),
]