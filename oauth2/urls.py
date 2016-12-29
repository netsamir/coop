"""oauth2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from coop_auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    #"GET /auth?code=edc64eb3aba308cdd25792c4088ac3e897f994cd&
    url(r'^auth.*', views.auth),
    url(r'^mycoop', views.mycoop, name='mycoop'),
]
