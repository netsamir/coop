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
    code = request.GET['code']
    data = {
        'client_id': 'Script_with_auth',
        'client_secret': 'fb765bad414da309eb7fc04bd1c2fac9',
        'grant_type':'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:9000/auth'
    }
    token_endpoint = "http://coop.apps.knpuniversity.com/token"
    token_endpoint_out = requests.post(token_endpoint, data=data)
    access_token = token_endpoint_out.json()['access_token']
    uri = 'http://coop.apps.knpuniversity.com/api/1270/eggs-collect'
    headers = {'Authorization': 'Bearer ' + access_token}
    eggs = requests.post(uri, headers=headers)
    return HttpResponse(eggs.text)
