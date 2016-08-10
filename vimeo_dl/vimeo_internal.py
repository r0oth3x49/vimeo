#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import time

if sys.version_info[:2] >= (3, 0):
    uni = str
else:
    uni = unicode

early_py_version = sys.version_info[:2] < (2, 7)

from .vimeo import fetch_decode
from .vimeo_shared import BaseVimeo, VimeoStream
from . import __version__, __author__
from .extractor import _extract_json,_extract_configs,_parse_config
from .compat import empty

class InternVimeo(BaseVimeo):
    def __init__(self, *args, **kwargs):
        self._info = []
        super(InternVimeo, self).__init__(*args, **kwargs)
        
    def _fetch_basic(self):
        if self._have_basic:
            return
        
        info = _extract_json(self._jsurl)
        self._title = info['title']
        self._author = info['user']
        self._viewcounts = info['viewed']
        self._user_id = info['user_id']
        
        self._likes = info['likes']
        self._comments = info['comments']
        self._username = info['user']
        t = int(info['duration'])
        (mins, secs) = divmod(t, 60)
        (hours, mins) = divmod(mins, 60)
        if hours == 0:
            self._duration = "%02d:%02d" % (mins, secs)
        else:
            self._duration = "%02d:%02d:%02d" % (hours, mins, secs)
        self._published = info['upload_date']

    def _fetch_data(self):
        if self._have_data:
            return
        
        conf = _extract_configs(self._conf_url)
        self._conf_file = conf
        self._info = _parse_config(self._conf_file, self.video_id)
            

    def _process_streams(self):
        if not self._have_basic:
            self._fetch_data()

        streams = [InternStream(z, self) for z in self._info['formats']]
        self._streams = streams
        empty("conf.json")

class InternStream(VimeoStream):

    def __init__(self, info, parent):
        super(InternStream, self).__init__(parent)

        self._itag = info['format_id']
        if (info.get('mime')) != 'none':
            self._mediatype = 'normal'
            self._extension = 'mp4'
            
        height = info.get('height') or 0
        width = info.get('width') or 0
        self._resolution = '%sx%s' % (width, height)
        self._dimention = width, height
        self._quality = self._resolution
        self._url = info.get('url')
        
        self._info = info

    

        
