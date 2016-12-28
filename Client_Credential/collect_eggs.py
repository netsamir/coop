#!/usr/bin/env python
"""Just a simple implementation of oauth2: Client Credential"""

import requests

def main():
    """Testing the application"""
    uri_token = 'http://coop.apps.knpuniversity.com/token'
    data = {
        'client_id': 'collect_eggs',
        'client_secret': 'aba08d307b6cbde2bb89cbbeff055e6b',
        'grant_type': 'client_credentials'
    }
    current_token = requests.post(uri_token, data=data)
    token = current_token.json()['access_token']
    uri = 'http://coop.apps.knpuniversity.com/api/1270/eggs-collect'
    headers = {'Authorization': 'Bearer ' + token}
    eggs = requests.post(uri, headers=headers)
    print(eggs.text)

if __name__ == '__main__':
    main()
