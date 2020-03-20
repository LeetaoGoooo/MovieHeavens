#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:test_app.py
"""

from unittest import TestCase
from movies import WorkThread

from movieSource.platforms.MovieHeaven import MovieHeavenPlatform
from movieSource.platforms.helper import get_all_platforms


class MockMovieSourceCombobox:

    def currentText(self):
        return "电影天堂"


class TestApp(TestCase):
    """测试app流程"""

    def test_get_all_platforms(self):
        all_platforms = get_all_platforms()
        self.assertTrue(MovieHeavenPlatform in all_platforms)

    def test_get_select_movie_source(self):
        thread = WorkThread()
        thread.movie_source_combobox = MockMovieSourceCombobox()
        search_movies, name, url, params = thread.get_select_movie_source("测试")
        self.assertEqual(name, "MovieHeaven")
