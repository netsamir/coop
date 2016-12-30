""" TEST """
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

import requests
from .models import CoopAuthToken

# Create your views here.

def home(request):
    """Home page"""
    # authorization_endpoint =
    url = "http://coop.apps.knpuniversity.com/authorize?client_id=Script_with_auth&response_type=code&redirect_uri=http://localhost:9000/auth&scope=eggs-collect profile eggs-count"
    access_token_valid = True
    user_id = 1270
    try:
        user = CoopAuthToken.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        user = CoopAuthToken.objects.create(user_id=user_id,\
                                     access_token='value missing',\
                                     expire_at=timezone.now())

    if user.expire_at < timezone.now():
        access_token_valid = False

    return render(request, 'coop_auth/home.html', {'access_token_valid': access_token_valid, 'url': url})

def mycoop(request):
    """ Check the status of my coop"""
    user_id = 1270
    domaine = "http://coop.apps.knpuniversity.com"

    user = CoopAuthToken.objects.get(user_id=user_id)
    access_token = user.access_token

    uri_profile = domaine + '/api/me'
    headers = {'Authorization': 'Bearer ' + access_token}

    profile = requests.get(uri_profile, headers=headers)
    user_id = profile.json()['id']

    uri_eggs_collect = '{}/api/{}/{}'.format(domaine, user_id, 'eggs-collect')
    uri_eggs_count = '{}/api/{}/{}'.format(domaine, user_id, 'eggs-count')

    eggs_collect = requests.post(uri_eggs_collect, headers=headers)
    eggs_count = requests.post(uri_eggs_count, headers=headers)
    result = "[{}, {}]".format(eggs_collect.text, eggs_count.text)
    return HttpResponse(result)

def auth(request):
    """Authorisation function"""
    domaine = "http://coop.apps.knpuniversity.com"
    user_id = 1270
    user = CoopAuthToken.objects.get(user_id=user_id)
    code = request.GET['code']
    data = {
        'client_id': 'Script_with_auth',
        'client_secret': 'fb765bad414da309eb7fc04bd1c2fac9',
        'grant_type':'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:9000/auth'
    }
    token_endpoint = domaine + "/token"
    token_endpoint_out = requests.post(token_endpoint, data=data)
    access_token = token_endpoint_out.json()['access_token']
    expires_in = token_endpoint_out.json()['expires_in']
    user.access_token = access_token
    user.expire_at = timezone.now() + timedelta(0, int(expires_in))
    user.save()

    return redirect('mycoop')
