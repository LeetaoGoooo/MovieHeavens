# -*- coding: utf-8 -*-
"""
    movieSource._compat
    ~~~~~~~~~~~~~
    用以兼容 py2/3
    
    :copyright: © 2018 by leetao.
    :license: GPL, see LICENSE for more details.
"""

import sys

PY2 = sys.version_info[0] == 2

import urllib

if PY2:
    def url_encode(values):
        return urllib.urlencode(values)

else:
    
    def url_encode(values):
        return urllib.parse.urlencode(values)