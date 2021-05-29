from django.urls import path
from .views import Main_Page_Card_Info
from Front.views import MainPage
from Front.views import Search
from .views import Generate_Paper_bibtex
from .views import Add_View_recoed
from .views import Add_Click_record
from Front.views import Recomend_and_cite_Paper_Page
from .views import Paper_Citation_Trend

urlpatterns = [
    path('CardInfo', Main_Page_Card_Info),
    path('mainpage', MainPage),
    path('search', Search),
    path('bib', Generate_Paper_bibtex),
    path('viewrecord', Add_View_recoed),
    path('clickrecord', Add_Click_record),
    path('paperpagerec', Recomend_and_cite_Paper_Page),
    path('ctrend', Paper_Citation_Trend)
]
