#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
from . import __version__, __author__
from .compat import (
    compat_opener,
    compat_urlerr,
    compat_httperr,
    )

Vimeo = None
backend = "internal"
def fetch_decode(url, encoding=None):
    """ Fetch url and decode. """
    try:
        req = compat_opener.open(url)
    except (compat_urlerr, compat_httperr) as e:
        if e.getcode() == 503:
            time.sleep(.5)
            return fetch_decode(url, encoding)
        else:
            raise
        
def new(url, basic=True, data=False, size=False, callback=None):
    """ Return a new vimeo instance given a url.

    Optional arguments:
        size - fetch the size of stream
        basic - fetch basic information of a given vimeo url
        callback - a callback function to receive status strings
    """
    global Vimeo
    if Vimeo is None:
        if backend == "internal":
            from .vimeo_internal import InternVimeo as Vimeo 
    return Vimeo(url, basic, data, size, callback)


