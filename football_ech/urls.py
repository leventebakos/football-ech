"""football_ech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import social_login.views
import leagues.views
import matches.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', social_login.views.login),
    url(r'^logout/$', social_login.views.logout),
    url(r'^leagues/create_league/$', leagues.views.create_league),
    url(r'^leagues/join_private_league/$', leagues.views.join_private_league),
    url(r'^leagues/join_league/$', leagues.views.list_available_leagues),
    url(r'^leagues/join_league/([0-9]+)/$', leagues.views.join_league),
    url(r'^leagues/my_leagues/$', leagues.views.get_my_leagues),
    url(r'^leagues/my_league/([0-9]+)/$', leagues.views.league_details),
    url(r'^leagues/([0-9]+)/tip/([0-9]+)/$', matches.views.maketips),
]