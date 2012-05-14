"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Views
"""
from .models import LimitedLink, LimitedLinkExpired
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext_lazy as _

def access_link(request, link_slug, template_name='tsj/link.haml'):
    """
    Renders link contents if accessible
    """
    link = get_object_or_404(LimitedLink, slug=link_slug)
    try:
        return direct_to_template(request, template_name, {'object': link.get_access()})
    except LimitedLinkExpired:
        return direct_to_template(request, template_name, {'error': _('link expired'), 'link': link})