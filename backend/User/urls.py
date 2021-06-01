from django.urls import path, re_path

from . import views


urlpatterns = [
    path('user_login', views.user_login),
    path('user_signup', views.user_signup),
    path('user_info', views.get_user_info),
    path('user_papers', views.get_user_papers),
    path('user_edu', views.get_user_edu_list),
    path('user_work', views.get_user_work_list),
    path('user_related_authors', views.get_user_related_authors)
]
