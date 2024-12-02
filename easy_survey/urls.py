from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from user_auth.views import  login_root_redirect
from results import views as result_view
from . import views as root_view
from create_form import views as create_form_view

urlpatterns = [
    path('', login_root_redirect, name='root_redirect'),
    path('home/', root_view.index, name='home'),
    path('admin/', admin.site.urls),
    path('admin/logout', auth_views.LogoutView.as_view(template_name='easy_survey/logout.html'), name='logout'),
    path('user/', include('user_auth.urls')),
    path('answers/', include('answers.urls')),
    path('results/', root_view.results, name='results'),
    path('published/', root_view.published, name='published'),
    path('republished/', root_view.republished, name='republished'),
    path('form/', include('create_form.urls')),
    
    path('<str:code>/responses', result_view.responses, name='responses'),
    path('<str:code>/response/<str:response_code>/edit', create_form_view.edit_response, name="edit_response"),
    path('<str:code>/responses/delete', create_form_view.delete_responses, name="delete_responses"),
    # 404 not found, 403 forbidden
    path('403', result_view.FourZeroThree, name="403"),
    path('404', result_view.FourZeroFour, name="404")
]

