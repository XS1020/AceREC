from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
# Create your views here.


def MainPage(request):
    Recom = [
        94747717, 172379530, 216802878, 223658030, 228111136,
        277256906, 448852786, 473532210, 111870135, 379921807
    ]
    dresponse = {
    	'Rec': Recom
    }
    return JsonResponse(dresponse)


