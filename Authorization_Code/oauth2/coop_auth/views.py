""" TEST """
from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def home(request):
    """Home page"""
    # authorization_endpoint = http://coop.apps.knpuniversity.com/authorize?client_id=Script_with_auth&response_type=code
    return render(request, 'home.html')

def auth(request):
    """Authorisation function"""
    domaine = "http://coop.apps.knpuniversity.com"
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
    uri_profile = domaine + '/api/me'
    headers = {'Authorization': 'Bearer ' + access_token}

    profile = requests.get(uri_profile, headers=headers)
    user_id = profile.json()['id']
    
    uri_eggs_collect = '{}/api/{}/{}'.format(domaine, user_id, 'eggs-collect')
    uri_eggs_count = '{}/api/{}/{}'.format(domaine, user_id, 'eggs-count')

    eggs_count = requests.post(uri_eggs_count, headers=headers)
    eggs_collect = requests.post(uri_eggs_collect, headers=headers)
    out = "Eggs Count: {} \n Eggs Collect: {}".format(eggs_count.text,
                                                      eggs_collect.text)
    return HttpResponse(out)
