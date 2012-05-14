"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Urls
"""
from django.conf.urls.defaults import patterns, include, url
from .views import preview_link, access_youtube_link

urlpatterns = patterns('',
    url(r'link/(?P<link_slug>.+)/$', preview_link, name='tsj_access_link'),
    url(r'video/(?P<link_slug>.+)/$', access_youtube_link, name='tsj_access_youtube_link'),
)