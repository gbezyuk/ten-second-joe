"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Views
"""
from .models import LimitedLink, LimitedLinkExpired, YoutubeLink
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _

def preview_link(request, link_slug, template_name='tsj/link.haml'):
    """
    Renders link preview
    """
    link = get_object_or_404(LimitedLink, slug=link_slug)
    if link.get_object_type() == YoutubeLink:
        template_name='tsj/youtube_link.haml'
    return direct_to_template(request, template_name, {'link': link})

def access_youtube_link(request, link_slug):
    """
    Renders link contents if accessible
    """
    link = get_object_or_404(LimitedLink, slug=link_slug)
    object = link.get_access()
    if object.__class__ == YoutubeLink:
        return object.renderer()
    else:
        raise AssertionError(_('Not a YouTube link'))