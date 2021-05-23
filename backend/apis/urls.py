from django.urls import path
from .views import Main_Page_Card_Info

urlpatterns = [
	path('CardInfo', Main_Page_Card_Info)
]