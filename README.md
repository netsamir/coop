# Introduction

Implementation of OAuth2 from KNP University using Python

- [RFC6749](https://tools.ietf.org/html/rfc6749 "Specifications")
- [OAuth2 in 8 steps](https://knpuniversity.com/screencast/oauth "Tutorial")

# Roles

## Ressource Owner

I have created an account with [KNP University](http://coop.apps.knpuniversity.com/api)

- Username: netsamir
- Password: xxxxxxxx

## Resource Server

[COOP](http://coop.apps.knpuniversity.com/api)

## Client

This is what I will try to implement

## Authorization server

It should be the same than the Ressource Server

# Protocol Flow

     +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+

                     Figure 1: Abstract Protocol Flow



> (A)  The client requests authorization from the resource owner.  The
>      authorization request can be made directly to the resource owner
>      (as shown), or preferably indirectly via the authorization
>      server as an intermediary.

Of course in our case we will use the "indirectly via the authorization server as intermediary

>(B)  The client receives an authorization grant, which is a
>     credential representing the resource owner's authorization,
>     expressed using one of four grant types defined in this
>     specification or using an extension grant type.  The
>     authorization grant type depends on the method used by the
>     client to request authorization and the types supported by the
>     authorization server.

In that case the `Authorization grant` will be an Authorization Code.

COOP accepts both `Authorization grant`:

- Authorization Code
- Client Credentials

Of course, the first one is the most complicated.  We will see it at the end.

# Client Credentials

>   The client credentials (or other forms of client authentication) can
>   be used as an authorization grant when the authorization scope is
>   limited to the protected resources under the control of the client,
>   or to protected resources previously arranged with the authorization
>   server.  Client credentials are used as an authorization grant
>   typically when the client is acting on its own behalf (the client is
>   also the resource owner) or is requesting access to protected
>   resources based on an authorization previously arranged with the
>   authorization server.

After having created my user account I have been assigned a USER ID.

- User ID: 1270

What is important here is that the Specification says that in the case of Client Credentials:

> based on an authorization previously arranged with the authorization server.

This means that we have to have a arrangement with the authorization server.

Let's say that we don't have one.

## Using cURL

We can have a simple test with cURL and POST

    Request : curl -X POST http://coop.apps.knpuniversity.com/api/2/eggs-collect
    Response: {"error":"access_denied","error_description":"an access token is required"}%

## Using the website

The exact same test can be done from the website directly [here](http://coop.apps.knpuniversity.com/application/api/eggs-collect)

Without Access Token the Post request is the following:

    POST /api/1270/eggs-collect HTTP/1.1
    Host: coop.apps.knpuniversity.com
    Authorization: Bearer ACCESSTOKENHERE

And the result will the same than the above cURL test that is :

    Response: {"error":"access_denied","error_description":"an access token is required"}%

## Access Token

As we have seen previously the authorization does not require anything from the Customers.

>   Access tokens are credentials used to access protected resources.  An
>   access token is a string representing an authorization issued to the
>   client.  The string is usually opaque to the client.  Tokens
>   represent specific scopes and durations of access, granted by the
>   resource owner, and enforced by the resource server and authorization
>   server.

Tokens represent **specific scopes and durations of access** granted by the ressource owner.

>   The token may denote an identifier used to retrieve the authorization
>   information or may self-contain the authorization information in a
>   verifiable manner (i.e., a token string consisting of some data and a
>   signature).  Additional authentication credentials, which are beyond
>   the scope of this specification, may be required in order for the
>   client to use a token.
>
>   The access token provides an abstraction layer, replacing different
>   authorization constructs (e.g., username and password) with a single
>   token understood by the resource server.  This abstraction enables
>   issuing access tokens more restrictive than the authorization grant
>   used to obtain them, as well as removing the resource server's need
>   to understand a wide range of authentication methods.

In the case of Client Credential. I, User ID : 1270, will register the application that will act on my behalf.

Here are the parameters:

- Application Name: First Script
- Redirect URI: *Not Applicable*
- Scope: Collect Eggs from Your Chickens

Further to this action the Authorization servers have provided me with the following information:

- Client ID: First Script
- Client Secret: 9fefdfe4e1dbff8e5ece8e148912ddea
- Redirect URI:
- Scope: eggs-collect

**Client ID and Client Secret are the Client Credential**

It is with the Client Credential that we will retrieve the token.

### Using cURL or the Website to generate the token

    ➜  coop git:(master) ✗ curl -X Post -d "client_id=First+Script&client_secret=9fefdfe4e1dbff8e5ece8e148912ddea&grant_type=client_credentials" http://coop.apps.knpuniversity.com/token
    {"access_token":"1a877fd91cef27900fa43289d1e63a293376bfde","expires_in":86400,"token_type":"Bearer","scope":"eggs-collect"}

## Retrieve the information
### Using cURL or the Website

    ➜  coop git:(master) ✗ curl -X POST -H "Authorization: Bearer 77629f07a9f600edd130ce851944f1b290af9f0e" http://coop.apps.knpuniversity.com/api/1270/eggs-collect
    {"action":"eggs-collect","success":true,"message":"Hey look at that, 5 eggs have been collected!","data":5}

Should we try to get the information of another user then we will get Error Message:

    ➜  coop git:(master) ✗ curl -X POST -H "Authorization: Bearer 77629f07a9f600edd130ce851944f1b290af9f0e" http://coop.apps.knpuniversity.com/api/2/eggs-collect
    {"error":"access_denied","error_message":"You do not have access to take this action on behalf of this user"}

## In Python

    #!/usr/bin/env python

    """Just a simple implementation oauth2: Client Credentials
    """

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

# Authorization Code

>   The authorization code is obtained by using an authorization server
>   as an intermediary between the client and resource owner.  Instead of
>   requesting authorization directly from the resource owner, the client
>   directs the resource owner to an authorization server (via its
>   user-agent as defined in [RFC2616]), which in turn directs the
>   resource owner back to the client with the authorization code.

>   Before directing the resource owner back to the client with the
>   authorization code, the authorization server authenticates the
>   resource owner and obtains authorization.  Because the resource owner
>   only authenticates with the authorization server, the resource
>   owner's credentials are never shared with the client.


Of course, this is what we want to do. The course provided by the Univerity allows use another type of Authorization grant: `Client Credentials`.

## Protocol Endpoints

>   The authorization process utilizes two authorization server endpoints
>   (HTTP resources):

>   o  Authorization endpoint - used by the client to obtain
>      authorization from the resource owner via user-agent redirection.

>   o  Token endpoint - used by the client to exchange an authorization
>      grant for an access token, typically with client authentication.
>
>   As well as one client endpoint:

>   o  Redirection endpoint - used by the authorization server to return
>      responses containing authorization credentials to the client via
>      the resource owner user-agent.

I have created another application and this time I have provided a redirect_uri

Client ID: Script_with_auth
Client Secret: fb765bad414da309eb7fc04bd1c2fac9
Redirect URI: http://localhost:9000/auth
Scope: eggs-count

### Authorization endpoint

http://coop.apps.knpuniversity.com/authorize?client_id=Script_with_auth&response_type=code

Retrieve the authorization code

GET /authorize	
When using the authorization code (traditional "web") grant type, start by redirecting the user to this URL:

http://coop.apps.knpuniversity.com/authorize
This accepts the following GET parameters

- client_id
- response_type Either code or token
- redirect_uri (authorization_code only) The URL that COOP will redirect the user back to after granting or denying authorization.
- scope The permissions the user should authorize, separated by a space (e.g. "eggs-count profile"). One of: 
    - barn-unlock 
    - toiletseat-down 
    - chickens-feed 
    - eggs-collect 
    - eggs-count 
    - profile

- (Optional) state A key that's returned on the redirect_uri that can be used as a CSRF token.

Once the user is redirected back to redirect_uri, you'll have a code query parameter. Use this with the next endpoint to exchange that code for an access token.


In our project we will use the following that will be in our home page:

<a href='http://coop.apps.knpuniversity.com/authorize?client_id=Script_with_auth&response_type=code&redirect_uri=http://localhost:9000/auth&scope=eggs-collect'>Authorize</a>

### Token endpoint

URL: Description
POST /token:

The endpoint used for requesting an access token, using either the authorization_code or client_credentials grant type.

http://coop.apps.knpuniversity.com/token
This accepts the following POST fields:

- client_id
- client_secret
- grant_type Either client_credentials or authorization_code
- redirect_uri (authorization_code only) Must match redirect_uri from the original /authorize call
- code (authorization_code only) The authorization code

## Django

For this implementation I will need a webserver able to handle redirct_uri.
I will implement it in Django using the Social Auth App Django:

    django-admin startproject oauth2
    django-admin startapp coop_auth

Add coop_auth in `INSTALLED_APPS`.

oauth2/urls.py:

    urlpatterns = [
        url(r'^auth.*', views.auth),
    ]

coop_auth/views.py:

    def auth(request):
        """Authorisation function"""
        return HttpResponse(request.GET['code'])

Now we could add
