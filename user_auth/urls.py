from django.urls import path
from user_auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', views.register, name='signup' ),
    path('login', auth_views.LoginView.as_view(template_name='easy_survey/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='easy_survey/logout.html'), name='logout'),
]