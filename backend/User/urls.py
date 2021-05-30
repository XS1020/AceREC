from django.urls import path, re_path

from . import views


urlpatterns = [
    path('user_login', views.user_login),
]
