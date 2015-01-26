from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import user_passes_test


login_forbidden = user_passes_test(lambda u: u.is_anonymous(), login_url='/')

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', login_forbidden(login),
         {'template_name': 'login.html'}),
    url(r'^logout', logout,
         {'next_page': '/'}),
    url(r'^', include('ui.urls')),
)