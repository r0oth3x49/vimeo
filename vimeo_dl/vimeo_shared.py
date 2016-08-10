#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
early_py_version = sys.version_info[:2] < (2, 7)
from . import __version__, __author__
from .compat import (
    compat_request,
    compat_urllib,
    compat_urlparse,
    compat_urlerr,
    compat_httperr,
    config,
    json_url,
    std_headers,
    json_read,
    json_fileread,
    compat_urlopen,
    compat_opener,
    user_agent,
    )

def extract_vid(url):
    try:
        url = compat_urlparse(url)
    except Exception as e:
        pass
    else:
        if len(url.path) > 1:
            video_id = url.path.replace('/', '')
        return video_id

def extract_json_url(vid):
    jsurl = json_url % vid
    return jsurl

def extract_config_url(vid):
    conf_url = config % vid
    return conf_url


class BaseVimeo(object):

    def __init__(self, url, basic=True, data=False, size=False, callback=None):

        self.video_id = extract_vid(url)
        self._jsurl = extract_json_url(self.video_id)
        self._conf_url = extract_config_url(self.video_id)

        self._callback = callback or (lambda x: None)
        self._have_basic = False
        self._have_data = False
        self._best = None

        self._streams = []
        
        self._likes = None
        self._comments = None
        self._published = None
        self._username = None

        self._title = None
        self._author = None
        self._duration = None
        self._viewcounts = None
        self._user_id = None

        if basic:
            self._fetch_basic()

        if data:
            self.fetch_data()

        if size:
            if not self._streams:
                self._process_streams()
            s = self._streams
            s.get_filesize()

    def _fetch_basic(self):
        raise NotImplementedError

    
    def _fetch_data(self):
        raise NotImplementedError

    def _process_streams(self):
        raise NotImplementedError

    @property
    def title(self):
        if not self._title:
            self._fetch_basic()
        return self._title

    @property
    def author(self):
        if not self._author:
            self._fetch_basic()
        return self._author

    @property
    def viewcounts(self):
        if not self._viewcounts:
            self._fetch_basic()
        return self._viewcounts

    @property
    def duration(self):
        if not self._duration:
            self._fetch_basic()
        return self._duration

    @property
    def username(self):
        if not self._username:
            self._fetch_basic()   
        return self._username

    @property
    def published(self):
        if not self._published:
            self._fetch_basic()
        return self._published

    @property
    def likes(self):
        if not self._likes:
            self._fetch_basic()
        return self._likes

    @property
    def comments(self):
        if not self._comments:
            self._fetch_basic()
        return self._comments

    @property
    def streams(self):
        if not self._streams:
            self._process_streams()
        return self._streams

    def _getbest(self):
        streams = self.streams
        if not streams:
            return None
        def _sortkey(x, keyres=0, keyftype=0):
            keyres = int(x.resolution.split('x')[0])
            keyftype = x.extension
            st = (keyftype, keyres)
            return st
        
        self._best = max(streams, key=_sortkey)
        return self._best

    def getbest(self):
        return self._getbest()
            

class VimeoStream(object):

    def __init__(self, parent):

        self._itag = None
        self._mediatype = None
        self._quality = None
        self._resolution = None
        self._dimention = None
        self._extension = None
        self._url = None

        self._parent = parent
        self._filename = None
        self._fsize = None
        self._active = False

    def __repr__(self):
        out = "%s:%s@%s" % (self.mediatype, self.extension, self.quality)
        return out

    def generate_filename(self):
        ok = re.compile(r'[^/]')

        if os.name == "nt":
            ok = re.compile(r'[^\\/:*?"<>|]')

        filename = "".join(x if ok.match(x) else "_" for x in self.title)
        filename += "." + self._extension
        
        return filename

    @property
    def resolution(self):
        return self._resolution

    @property
    def quality(self):
        return self._quality

    @property
    def url(self):
        return self._url

    @property
    def dimention(self):
        return self._dimention

    @property
    def extension(self):
        return self._extension

    @property
    def filename(self):
        if not self._filename:
            self._filename = self.generate_filename()
        return self._filename

    @property
    def title(self):
        return self._parent.title

    @property
    def mediatype(self):
        return self._mediatype

    def get_filesize(self):
        if not self._fsize:
            try:
                cl = 'content-length'
                opener = compat_opener()
                opener.addheaders = [('User-Agent', user_agent)]
                self._fsize = int(opener.open(self.url).headers[cl])
            except (compat_urlerr, compat_httperr):
                self._fsize = 0
                
        return self._fsize

    def cancel(self):
        if self._active:
            self._active = True
            return True


    def download(self, filepath="", quiet=False, callback=lambda *x: None):
        savedir = filename = ""

        if filepath and os.path.isdir(filepath):
            savedir, filename = filepath, self.generate_filename()

        elif filepath:
            savedir, filename = os.path.split(filepath)

        else:
            filename = self.generate_filename()

        filepath = os.path.join(savedir, filename)
        temp_filepath = filepath + ".temp"

        status_string = ('  {:,} Bytes [{:.2%}] received. Rate: [{:4.0f} '
                         'KB/s].  ETA: [{:.0f} secs]')


        if early_py_version:
            status_string = ('  {0:} Bytes [{1:.2%}] received. Rate:'
                             ' [{2:4.0f} KB/s].  ETA: [{3:.0f} secs]')

        try:    
            req = compat_request(self.url, headers=std_headers)
            response = compat_urlopen(req)
        except (compat_urlerr, compat_httperr) as e:
            return e
        else:
            total = int(response.info()['Content-Length'].strip())
            chunksize, bytesdone, t0 = 16384, 0, time.time()

            fmode, offset = "wb", 0

            if os.path.exists(temp_filepath):
                if os.stat(temp_filepath).st_size < total:
                    offset = os.stat(temp_filepath).st_size
                    fmode = "ab"

            outfh = open(temp_filepath, fmode)

            if offset:
                resume_opener = compat_opener()
                resume_opener.addheaders = [('User-Agent', user_agent),
                                            ("Range", "bytes=%s-" % offset)]
                try:
                    response = resume_opener.open(self.url)
                except (compat_urlerr, compat_httperr) as e:
                    return e
                else:
                    bytesdone = offset

            self._active = True
            while self._active:
                chunk = response.read(chunksize)
                outfh.write(chunk)
                elapsed = time.time() - t0
                bytesdone += len(chunk)
                if elapsed:
                    rate = ((float(bytesdone) - float(offset)) / 1024.0) / elapsed
                    eta  = (total - bytesdone) / (rate * 1024)
                else:
                    rate = 0
                    eta = 0
                progress_stats = (bytesdone, bytesdone * 1.0 / total, rate, eta)

                if not chunk:
                    outfh.close()
                    break
                if not quiet:
                    status = status_string.format(*progress_stats)
                    sys.stdout.write("\r" + status + ' ' * 4 + "\r")
                    sys.stdout.flush()

                if callback:
                    callback(total, *progress_stats)

            if self._active:
                os.rename(temp_filepath, filepath)
                return filepath
            
            else:
                outfh.close()
                return temp_filepath
        
