from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    re_path(r'^submit/expense/$', views.submit_expense, name = 'submit_expense'),
    re_path(r'^submit/income/$', views.submit_income, name = 'submit_income'),
    path('', views.index, name ='index'),
    #path('register/', views.RegisterView.as_view(), name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='web/login.html'), name='login'),
    #path('profile/', views.ProfileView.as_view(), name='profile'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
