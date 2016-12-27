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
 >    |        |--(A)- Authorization Request ->|   Resource    |
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

## Authorization Code

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

## Client Credentials

>   The client credentials (or other forms of client authentication) can
>   be used as an authorization grant when the authorization scope is
>   limited to the protected resources under the control of the client,
>   or to protected resources previously arranged with the authorization
>   server.  Client credentials are used as an authorization grant
>   typically when the client is acting on its own behalf (the client is
>   also the resource owner) or is requesting access to protected
>   resources based on an authorization previously arranged with the
>   authorization server.

For the moment I don't see the point of using this mechanism.  But I will follow the course anyhow.

After having created my user account I have been assigned a USER ID.

    User ID: 1270

We can have a simple test with cURL and POST

    Request : curl -X POST http://coop.apps.knpuniversity.com/api/2/eggs-collect
    Response: {"error":"access_denied","error_description":"an access token is required"}%

The exact same test can be done from the website directly [here](http://coop.apps.knpuniversity.com/application/api/eggs-collect)

Without Access Token the Post request is the following:

    POST /api/1270/eggs-collect HTTP/1.1
    Host: coop.apps.knpuniversity.com
    Authorization: Bearer ACCESSTOKENHERE

And the result will the same than the above cURL test that is :

    Response: {"error":"access_denied","error_description":"an access token is required"}%

# Client Registration

# The client Credentials


