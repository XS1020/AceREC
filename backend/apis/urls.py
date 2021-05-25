from django.urls import path
from .views import Main_Page_Card_Info
from Front.views import MainPage
from Front.views import Search

urlpatterns = [
    path('CardInfo', Main_Page_Card_Info),
    path('mainpage', MainPage)
    path('search', Search)
]
