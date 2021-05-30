from django.urls import path, re_path

from . import views


urlpatterns = [
    path('user_login', views.user_login),
    path('user_info', views.get_user_info)
]
