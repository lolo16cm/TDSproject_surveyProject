from django.urls import path
from create_form import views
urlpatterns=[
    path('create', views.create_form, name="create_form"),
    path('<str:code>/edit', views.edit_form, name="edit_form"),
    path('<str:code>/edit_title', views.edit_title, name="edit_title"),
    path('<str:code>/edit_description', views.edit_description, name="edit_description"),
    path('<str:code>/edit_setting', views.edit_setting, name="edit_setting"),    
    path('<str:code>/delete', views.delete_form, name="delete_form"),
    path('<str:code>/edit_question', views.edit_question, name="edit_question"),
    path('<str:code>/edit_choice', views.edit_choice, name="edit_choice"),
    path('<str:code>/add_choice', views.add_choice, name="add_choice"),
    path('<str:code>/remove_choice', views.remove_choice, name="remove_choice"),
    path('<str:code>/get_choice/<str:question>', views.get_choice, name="get_choice"),
    path('<str:code>/add_question', views.add_question, name="add_question"),
    path('<str:code>/delete_question/<str:question>', views.delete_question, name="delete_question"),
    path('<str:code>/publish_form', views.publish_form, name="publish_form"),
    path('<str:code>/close_form', views.close_form, name="close_form"),
    path('<str:code>/republish_form', views.republish_form, name="republish_form"),
    path('<str:code>/viewform', views.view_form, name="view_form"),
    path('<str:code>/submit', views.submit_form, name="submit_form"),




]