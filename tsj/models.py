"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Views
"""
from django.db import models
import urllib
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
import sys

class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101230 Mandriva Linux/1.9.2.13-0.2mdv2010.2 (2010.2) Firefox/3.6.13"

class YoutubeLink(models.Model):
    """
    Main link class
    """
    # url is string that consists of symbols in parameter v
    url = models.CharField(max_length=255)
    video_cache = models.CharField(max_length=255, null=True, blank=True)

    def get_video_link(self):
        """
        We parse youtube link and set direct link to video file
        """
        if self.video_cache:
            return self.video_cache
        else:
            opener = AppURLopener()
            fp = opener.open('http://www.youtube.com/get_video_info?video_id={vid}'.format(vid = video_id))
            data = fp.read()
            fp.close()

            if data.startswith('status=fail'):
                raise Exception('Error: Video not found!')

            vid_list = []
            tmp_list = urllib.unquote(urllib.unquote(data)).split(',')
            for fmt_chk in tmp_list:
                if len(fmt_chk) == 0 or not fmt_chk.startswith('url=') and 'flv' not in fmt_chk:
                    continue
                vid_list.append(fmt_chk[4:])

            try:
                self.video_cache = vid_list[0]
                self.save()
            except ValueError:
                print 'Failed to parse video urls'
        
            return self.video_cache

    def renderer(self):
        """
        Renders link (HTML) view
        """
        raise NotImplementedError

class LimitedLink(models.Model):
    """
    A link with the limited number of uses model
    """
    #link slug
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=False, verbose_name=_('slug'))

    # activity status and logging
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))
    usages_left = models.PositiveIntegerField(default=0, verbose_name=_('usages left'), blank=False, null=False)
    usages_count = models.PositiveIntegerField(default=0, verbose_name=_('usages count'), blank=False, null=False)

    #generic foreign key fields bellow
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%d. %s - %s" % (self.pk, self.slug, self.content_object.__unicode__())