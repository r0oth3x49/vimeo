#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
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
    user_agent,
    compat_opener,
    conf_file,
    )
    
def _extract_json(url):
    json_info = {}
    try:
        req_json = compat_request(url, headers=std_headers)
        resp_json = compat_urlopen(req_json)
        
    except (compat_urlerr, compat_httperr) as e:
        return e
    else:
        jdata = resp_json.read().decode('utf-8')
        json = json_read(jdata)
        json_info = {
            "title"         : json[0]['title'],
            "user"          : json[0]['user_name'],
            "privacy"       : json[0]['embed_privacy'],
            "height"        : json[0]['height'],
            "width"         : json[0]['width'],
            "upload_date"   : json[0]['upload_date'],
            "likes"         : json[0]['stats_number_of_likes'],
            "comments"      : json[0]['stats_number_of_comments'],
            "user_url"      : json[0]['user_url'],
            "video_id"      : json[0]['id'],
            "duration"      : json[0]['duration'],
            "user_id"       : json[0]['user_id'],
            "url"           : json[0]['url'],
            "viewed"        : json[0]['stats_number_of_plays'],
            }
        return json_info


def _extract_configs(url):
    try:
        req_conf = compat_request(url, headers=std_headers)
        resp_conf = compat_urlopen(req_conf)
    except (compat_urlerr, compat_httperr) as e:
        return e
    else:
        if resp_conf.code == 200:
            conf_data = resp_conf.read()
            fd = open(conf_file,"wb")
            fd.write(conf_data)
            fd.close()
            return conf_file
        else:
            pass

def _parse_config(config, video_id):
    conf_info = {}
    fd = open(config)
    conf = json_fileread(fd)
    video_title = conf['video']['title']
    video_duration = conf['video'].get('duration')
    video_uploader = conf['video'].get('owner', {}).get('name')
    video_uploader_url = conf['video'].get('owner', {}).get('url')
    video_uploader_id = video_uploader_url.split('/')[-1] if video_uploader_url else None
    video_thumbnail = conf['video'].get('thumbnail')
    if video_thumbnail is None:
        video_thumbs = conf['video'].get('thumbs')
        if video_thumbs and isinstance(video_thumbs, dict):
            _, video_thumbnail = sorted((int(width if width.isdigit() else 0), t_url) for (width, t_url) in video_thumbs.items())[-1]

    formats = []
    config_files = conf['video'].get('files') or conf['request'].get('files', {})
    for f in config_files.get('progressive', []):
        video_url = f.get('url')
        if not video_url:
            continue
        formats.append({
            'url': video_url,
            'format_id' : f.get('quality'),
            'width'     : f.get('width'),
            'height'    : f.get('height'),
            'fps'       : f.get('fps'),
            'mime'      : f.get('mime'),
        })

    conf_info = {
        'title'       : video_title,
        'uploader'    : video_uploader,
        'uploader_id' : video_uploader_id,
        'uploader_url': video_uploader_url,
        'thumbnail'   : video_thumbnail,
        'duration'    : video_duration,
        'formats'     : formats,
        }
    return conf_info

