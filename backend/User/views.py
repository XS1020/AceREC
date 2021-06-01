import os
import time
import datetime
import hashlib

import django
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
import pygame
import numpy as np
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
        return HttpResponse('User name or password wrong!', status=401)

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
        info['user_name'] = u.user_name
    else:
        return HttpResponse('User name or password wrong!', status=401)
    return JsonResponse(info)

def user_signup(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    u_name = req.get('user_name', None)
    pwd = req.get('password', None)
    affiliation = req.get('affiliation', None)

    if u_name is None:
        return HttpResponseBadRequest('Need user name!')
    if pwd is None:
        return HttpResponseBadRequest('Need password!')
    if affiliation is None:
        return HttpResponseBadRequest('Need affiliation!')

    # check the uniqueness of the name
    tmp = models.User_Info.objects.filter(user_name=u_name)
    if len(tmp) > 0:
        return HttpResponse('User name already exist!', status=405)

    # generate local_id
    # local_id = models.User_Info.objects.count()
    last_user = models.User_Info.objects.order_by('local_id').reverse()[0]
    local_id = last_user.local_id + 1
    # print(local_id)

    try:
        models.User_Info.objects.create(
            local_id=local_id,
            remote_id=-1,
            name='',
            user_name=u_name,
            affiliation=affiliation,
            research_list='',
            password=pwd,
            paper_num=0
        )
    except django.db.utils.IntegrityError:
        return HttpResponseBadRequest('Registeration Failed!')

    login_time = int(time.time())
    token = generate_token(u_name, login_time)
    if models.User_Token.objects.filter(local_id=local_id).update(token=token, update_time=login_time):
        pass
    else:
        models.User_Token.objects.create(local_id=local_id, token=token, update_time=login_time)
    info = dict()
    info['local_id'] = local_id
    info['remote_id'] = -1
    info['token'] = token
    info['user_name'] = u_name

    return JsonResponse(info)

def get_user_info(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    local_id = req.get('local_id', None)

    if local_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        local_id = int(local_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid local ID!')

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

    chr = pin_name[0][0].upper()
    pygame.init()
    font = pygame.font.Font(os.path.join(avatar_dir, "font", "msyh.ttc"), 64)
    rtext = font.render(chr, True, (147, 112, 219), (255, 255, 255))
    pygame.image.save(rtext, avatar_path)

    info['avatar_url'] = '{}://{}/static/avatar/{}'.format(
        request.scheme, request.get_host(), avatar_name
    )

    return JsonResponse(info)


def get_user_papers(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    local_id = req.get('local_id', None)

    if local_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        local_id = int(local_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid local ID!')

    papers = models.User_Papers.objects.filter(local_id=local_id)
    paper_list = []
    for paper in papers:
        paper_list.append(paper.paper_id)

    info = {
        'paper_list': paper_list
    }

    return JsonResponse(info)

def get_user_edu_list(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    local_id = req.get('local_id', None)

    if local_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        local_id = int(local_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid local ID!')

    edus = models.User_Edu.objects.filter(local_id=local_id).order_by('-year')
    edu_list = []
    for edu in edus:
        e = dict()
        e['year'] = edu.year
        e['action'] = edu.action
        e['institute'] = edu.institute
        e['department'] = edu.department
        edu_list.append(e)

    info = {
        'edu_list': edu_list
    }

    return JsonResponse(info)

def get_user_work_list(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    local_id = req.get('local_id', None)

    if local_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        local_id = int(local_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid local ID!')

    works = models.User_Work.objects.filter(local_id=local_id).order_by('-year')
    work_list = []
    for work in works:
        w = dict()
        w['year'] = work.year
        w['action'] = work.action
        w['institute'] = work.institute
        w['department'] = work.department
        work_list.append(w)

    info = {
        'work_list': work_list
    }

    return JsonResponse(info)

def get_user_related_authors(request):
    req = request.GET

    if not req:
        return HttpResponseBadRequest('No Information!')

    target_id = req.get('local_id', None)

    if target_id is None:
        return HttpResponseBadRequest('Need local ID!')

    try:
        target_id = int(target_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid local ID!')

    idx2id = []  # index to local_id
    id2idx = dict()  # local_id to index
    paper_count = []  # index to num of papers

    papers = models.User_Papers.objects.filter(local_id=target_id)
    for paper in papers:
        co_authors = models.User_Papers.objects.filter(paper_id=paper.paper_id)
        for au in co_authors:
            au_id = au.local_id
            if au_id != target_id:
                if au_id in idx2id:
                    paper_count[id2idx[au_id]] = paper_count[id2idx[au_id]] + 1
                else:
                    au_idx = len(idx2id)
                    id2idx[au_id] = au_idx
                    idx2id.append(au_id)
                    paper_count.append(1)

    # select 4 co-authors
    related_authors = []
    if len(paper_count) > 4:
        paper_count = np.array(paper_count)
        idxes = np.argpartition(paper_count, -4)[-4:]
        idxes = idxes[::-1]
        for idx in idxes:
            au_local_id = idx2id[idx]
            related_authors.append(au_local_id)
    else:
        for au_local_id in idx2id:
            related_authors.append(au_local_id)

    info = {
        'related_authors': related_authors
    }

    return JsonResponse(info)
