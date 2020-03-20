#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:test_command.py
"""
from unittest import TestCase
from movieSource.commands.search_movie import SearchMovieCommand
from movieSource.platforms.MovieHeaven import MovieHeavenPlatform


class TestCommand(TestCase):

    def test_get_movie_platform(self):
        """测试获取电影平台"""
        self.assertEqual(MovieHeavenPlatform,
                         SearchMovieCommand.get_platform_by_name("MovieHeaven"))

