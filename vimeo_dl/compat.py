#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[:2] >= (3, 0):
    from json import loads as json_read
    from json import load as json_fileread
    from os import remove as empty
    import urllib.request as compat_urllib
    from urllib.request import Request as compat_request
    from urllib.request import urlopen as compat_urlopen
    from urllib.error import HTTPError as compat_httperr
    from urllib.error import URLError as compat_urlerr
    from urllib.parse import urlparse as compat_urlparse
    from urllib.request import build_opener as compat_opener
    uni, pyver = str, 3
    
else:
    from json import loads as json_read
    from json import load as json_fileread
    from os import remove as empty
    import urllib2 as compat_urllib
    from urllib2 import Request as compat_request
    from urllib2 import urlopen as compat_urlopen
    from urllib2 import URLError as compat_urlerr
    from urllib2 import HTTPError as compat_httperr
    from urlparse import urlparse as compat_urlparse
    from urllib2 import build_opener as compat_opener
    uni, pyver = unicode, 2


json_url = "http://vimeo.com/api/v2/video/%s.json"
config = "https://player.vimeo.com/video/%s/config"
conf_file = "conf.json"
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)"
std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
    }

__ALL__ =[
    "compat_request",
    "compat_urllib",
    "compat_urlparse",
    "compat_urlerr",
    "compat_httperr",
    "json_read",
    "config",
    "json_url",
    "std_headers",
    "json_fileread",
    "compat_urlopen",
    "compat_opener",
    "user_agent",
    "conf_file",
    "empty",
    ]
