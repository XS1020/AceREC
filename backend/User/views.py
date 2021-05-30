import time
import datetime
import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.core import signing

from . import models


# CONSTANTS
TIME_OUT = 60 * 60

# Create your views here.

def generate_token(name, t):
    input = name + str(t) + str(datetime.datetime.now())
    token = hashlib.md5(input.encode('utf-8')).hexdigest()
    return token

def user_login(request):
    req = request.GET()

    if not req:
        return HttpResponseBadRequest('No Information!')

    u_name = req.get('user_name', None)
    pwd = req.get('password', None)

    if u_name is None:
        return HttpResponseBadRequest('Please enter your user name!')
    if pwd is None:
        return HttpResponseBadRequest('Please enter the password!')

    # should use try here
    u = models.User_Info.objects.get(user_name=u_name)

    info = dict()
    if u.password == pwd:
        login_time = int(time.time())
        token = generate_token(u.user_name, login_time)
        if models.User_Token.objects.filter(local_id=u.local_id).update(token=token, update_time=login_time):
            pass
        else:
            models.User_Token.objects.create(local_id=u.local_id, token=token, update_time=login_time)
        info['local_id'] = u.local_id
        info['remote_id'] = u.remote_id
        info['token'] = token
    else:
        info['local_id'] = -1
        info['remote_id'] = -1
        info['token'] = -1
    return JsonResponse(info)
