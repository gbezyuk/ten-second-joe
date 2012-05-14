# encoding: utf-8
from django.db import models
import urllib
import sys


class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101230 Mandriva Linux/1.9.2.13-0.2mdv2010.2 (2010.2) Firefox/3.6.13"

class Link(models.Model):
    """
    main link class
    """
    url = models.ChardField(max_length=255)
    video_cache = models.CharField(max_length=255, null=True, blank=True)    

    def get_video_link(self):
        if not self.video_cache:
            opener = AppURLopener()
            fp = opener.open('http://www.youtube.com/get_video_info?video_id={vid}'.format(vid = video_id))
            data = fp.read()
            fp.close()

            if data.startswith('status=fail'):
                raise Exception('Error: Video not found!')


        
    
