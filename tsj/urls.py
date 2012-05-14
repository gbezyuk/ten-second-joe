"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Urls
"""
from django.conf.urls.defaults import patterns, include, url
from .views import access_link

urlpatterns = patterns('',
    url(r'(?P<link_slug>.+)/$', access_link, name='tsj_access_link')
)