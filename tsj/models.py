"""
Studio: ActionLearning.Ru
Authors: Andrew Sinitsyn, Grigoriy Beziuk
Project: Ten Second Joe
Module: Ten Second Joe
Part: Views
"""
from django.db import models
import urllib
import sys
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101230 Mandriva Linux/1.9.2.13-0.2mdv2010.2 (2010.2) Firefox/3.6.13"


class FLVWrapper(FileWrapper, object):
    """
    Wrapper for flx stream that implements iterator for httpresponse
    """
    def __init__(self, filelike):
        self.first_time = True
        super(FLVWrapper, self).__init__(filelike)


    def next(self):
        if not self.first_time: 
            data = self.filelike.read(self.blksize) 
        else:
            # correct flv format first bytes 
            data = "FLV\x01\x01\x00\x00\x00\x09\x00\x00\x00\x09" 
            data += self.filelike.read(self.blksize) 
            self.first_time = False 
        if data: 
            return data 
        raise StopIteration  


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
            fp = opener.open('http://www.youtube.com/get_video_info?video_id={vid}'.format(vid = self.url))
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
        opener = AppURLopener()
        filelike = opener.open(self.get_video_link())
        
        response = HttpResponse(FLVWrapper(filelike), mimetype='video/x-flv')
        response['Content-Length'] = filelike.info().__dict__['dict']['content-length']
        return response
