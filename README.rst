Features
--------

- Retreive metadata such as viewcount, duration, author, title, likes, comments
- Retrieve the URL to stream the video in a player such as vlc or mplayer
- Small, standalone, single importable module file (vimeo.py)
- Select highest quality stream for download
- Works with Python 2.6+ and 3.3+

Installation
------------

vimeo can be installed using `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

    $ [sudo] pip install vimeo_dl
	
Usage Examples
--------------

Here is how to use the module in your own python code.  For command line tool

.. code-block:: pycon

    >>> import vimeo_dl as vimeo

create a video instance from a Vimeo url:

.. code-block:: pycon

    >>> url = "https://vimeo.com/140816903"
    >>> video = vimeo.new(url)

get certain attributes:

.. code-block:: pycon
    
    >>> video.title
    '[PHP][C++]Root Exploiter - No Back-Connect (Part 2)'

    >>> video.viewcounts, video.author, video.likes
    (647, u'Mukarram Khalid', 0)

    >>> video.author, video.duration
    ('Mukarram Khalid', '10:00')
    
list available streams for a video:

.. code-block:: pycon

    >>> streams = video.streams
    >>> for s in streams:
    ...     print(s)
    ...
    normal:mp4@1162x720
    normal:webm@640x398
    
Download video with specific stream number:

.. code-block:: pycon

    >>> streams[0].download(quiet=False)
    163,840 Bytes [0.56%] received. Rate: [ 275 KB/s].  ETA: [104 secs]
    
get best resolution for a video:

.. code-block:: pycon

    >>> best = video.getbest()
    >>> best.resolution, best.extension
    ('1162x720', 'mp4')
	
get url, for download or streaming in mplayer / vlc etc:

.. code-block:: pycon
    
    >>> best.url
    'https://fpdl.vimeocdn.com/vimeo-prod-skyfire-std-us/01/3163/5/140816903/421224858...'
	
Download video and show progress:

.. code-block:: pycon

    >>> best.download(quiet=False)
    212,992 Bytes [2.64%] received. Rate: [ 203 KB/s].  ETA: [38 secs]
