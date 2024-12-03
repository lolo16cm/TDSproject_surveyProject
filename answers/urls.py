

from django.urls import path
from answers import views


urlpatterns = [
    path('<str:code>/response/<str:response_code>', views.response, name="response"),

]