#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" setup.py for vimeo.

python setup.py sdist bdist_wheel

"""

from setuptools import setup
from vimeo_dl import __version__

setup(
    name='vimeo_dl',
    packages=['vimeo_dl'],
    version=__version__,
    description="Retrieve Vimeo content and metadata",
    keywords=["vimeo_dl", "download", "video"],
    author="Nasir khan (r0ot h3x49)",
    author_email="r0ot@h3x49@gmail.com",
    url = "https://github.com/r0oth3x49/vimeo",
    download_url="https://github.com/r0oth3x49/vimeo/tarball/master",
    package_data={"": ["LICENSE","README.rst", "AUTHOR"]},
    include_package_data=True,
    license='LGPLv3',
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 "
        "(LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS 9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"],
    long_description=open("README.rst").read()
)
