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

It is said in the Website that it COOP accepts both `Authorization grant`:

- Authorization Code
- Client Credentials

Of course, the first one is the most complicated.  We will see it at the end.

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

This means that we have to have a arrangement with the authorization server.  Let's that we don't have one.

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

As we have seen previously the authorization does not required anything from the Customers.

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


### Using cURL or the Website

    ➜  coop git:(master) ✗ curl -X Post -d "client_id=First+Script&client_secret=9fefdfe4e1dbff8e5ece8e148912ddea&grant_type=client_credentials" http://coop.apps.knpuniversity.com/token
    {"access_token":"1a877fd91cef27900fa43289d1e63a293376bfde","expires_in":86400,"token_type":"Bearer","scope":"eggs-collect"}

## Retrieve the information
### Using cURL or the Website

    ➜  coop git:(master) ✗ curl -X POST -H "Authorization: Bearer 77629f07a9f600edd130ce851944f1b290af9f0e" http://coop.apps.knpuniversity.com/api/1270/eggs-collect
    {"action":"eggs-collect","success":true,"message":"Hey look at that, 5 eggs have been collected!","data":5}
    ➜  coop git:(master) ✗

Should we try to get the information of another user then we will get Error Message:

    coop git:(master) ✗ curl -X POST -H "Authorization: Bearer 77629f07a9f600edd130ce851944f1b290af9f0e" http://coop.apps.knpuniversity.com/api/2/eggs-collect
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
