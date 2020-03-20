#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:search_movie.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2017 by the eigen.
    :license: BSD, see LICENSE for more details.
"""
from movieSource.platforms.helper import import_the_platform


class SearchMovieCommand:

    @staticmethod
    def get_platform_by_name(name):
        platform = import_the_platform(name)
        if not platform:
            raise ValueError("无效的平台名称")
        return platform

    def execute(self, name, *args, **kwargs):
        platform = self.get_platform_by_name(name)
        return platform.get_display_content(*args, **kwargs)


if __name__ == '__main__':
    print(SearchMovieCommand.get_platform_by_name("MovieHeaven"))