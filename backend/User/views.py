import os
import time
import datetime
import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
import pygame
from pypinyin import lazy_pinyin

from . import models
from backend.settings import STATICFILES_DIRS


# CONSTANTS
TIME_OUT = 60 * 60

# Create your views here.

def generate_token(name, t):
    input = name + str(t) + str(datetime.datetime.now())
    token = hashlib.md5(input.encode('utf-8')).hexdigest()
    return token

def user_login(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    u_name = req.get('user_name', None)
    pwd = req.get('password', None)

    if u_name is None:
        return HttpResponseBadRequest('Please enter your user name!')
    if pwd is None:
        return HttpResponseBadRequest('Please enter the password!')

    try:
        u = models.User_Info.objects.get(user_name=u_name)
    except models.User_Info.DoesNotExist:
        return HttpResponseBadRequest('No such user!')

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

def get_user_info(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    local_id = req.get('local_id', None)

    if local_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        u = models.User_Info.objects.get(local_id=local_id)
    except models.User_Info.DoesNotExist:
        return HttpResponseBadRequest('No such user!')

    info = dict()
    info['name'] = u.name
    pin_name = lazy_pinyin(u.name)
    info['pinyin'] = pin_name
    info['affiliation'] = u.affiliation
    research_list = u.research_list
    research_list = research_list.split("_")
    info['research_list'] = research_list
    info['paper_num'] = u.paper_num

    # generate avatar
    avatar_dir = os.path.join(STATICFILES_DIRS[0], 'avatar')
    avatar_name = '{}.png'.format(local_id)
    avatar_path = os.path.join(avatar_dir, avatar_name)

    chr = pin_name[0].upper()
    pygame.init()
    font = pygame.font.Font(os.path.join(avatar_dir, "msyh.ttc"), 64)
    rtext = font.render(chr, True, (0, 0, 0), (255, 255, 255))
    pygame.image.save(rtext, avatar_path)

    info['avatar_url'] = '{}://{}/static/avatar/{}'.format(
        request.scheme, request.get_host(), avatar_name
    )

    return JsonResponse(info)
