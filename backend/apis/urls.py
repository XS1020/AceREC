from django.urls import path
from .views import Main_Page_Card_Info
from Front.views import MainPage
from Front.views import Search
from .views import Generate_Paper_bibtex

urlpatterns = [
    path('CardInfo', Main_Page_Card_Info),
    path('mainpage', MainPage),
    path('search', Search),
    path('bib', Generate_Paper_bibtex)
]
