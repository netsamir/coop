"""
An Implementation of OAuth2 according to RFC649 and
https://knpuniversity.com/screencast/oauth.
"""
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

import requests
from .models import CoopAuthToken

# Create your views here.

def home(request):
    """
    Authorization Server:
      The server issuing access tokens to the client after successfully
      authenticating the resource owner and obtaining authorization.

   (A)  The client requests authorization from the resource owner.  The
        authorization request can be made [...] indirectly via the
        authorization server as an intermediary.
    """
    context = {}
    # authorization_endpoint =
    authorize = {
        'base_url' : "http://coop.apps.knpuniversity.com/authorize",
        'client_id' : "Script_with_auth",
        'response_type' : "code",
        'redirect_uri' : "http://localhost:9000/auth",
        'scope' : "eggs-collect profile eggs-count"
    }

    url = "{base_url}?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_uri}&scope={scope}".format(**authorize)

    access_token_valid = True
    user_id = 1270
    try:
        user = CoopAuthToken.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        user = CoopAuthToken.objects.create(user_id=user_id,\
                                     access_token='value missing',\
                                     expire_at=timezone.now() - timedelta(0, 1483272159))

    expire_in = (user.expire_at - timezone.now()).total_seconds()
    if expire_in < 120: #120 seconds
        access_token_valid = False

    context = {\
        'access_token_valid': access_token_valid,\
        'url': url,\
        'expire_in': expire_in\
    }

    return render(request, 'coop_auth/home.html', context)

def mycoop(request):
    """ Check the status of my coop

   (E)  The client requests the protected resource from the resource
        server and authenticates by presenting the access token.

   (F)  The resource server validates the access token, and if valid,
        serves the request.
    """
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
    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    result = '[{}, {}, {{"last_update": "{}"}}]'.format(eggs_collect.text, eggs_count.text, now)
    return HttpResponse(result)

def auth(request):
    """
    Authorization Server:
      The server issuing access tokens to the client after successfully
      authenticating the resource owner and obtaining authorization.

   (B)  The client receives an authorization grant, which is a
        credential representing the resource owner's authorization, [...]. The
        authorization grant type depends on the method used by the
        client to request authorization and the types supported by the
        authorization server.

   (C)  The client requests an access token by authenticating with the
        authorization server and presenting the authorization grant.

   (D)  The authorization server authenticates the client and validates
        the authorization grant, and if valid, issues an access token.
    """
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
    # token_endpoint =
    token_endpoint = domaine + "/token"
    token_endpoint_out = requests.post(token_endpoint, data=data)
    print(token_endpoint_out.text)
    access_token = token_endpoint_out.json()['access_token']
    expires_in = token_endpoint_out.json()['expires_in']
    user.access_token = access_token
    user.expire_at = timezone.now() + timedelta(0, int(expires_in))
    user.save()

    return redirect('home')
