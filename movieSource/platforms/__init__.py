#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long

from abc import abstractmethod, ABCMeta
from movieSource.fake_user_agent import useragent_random


class BasePlatform(metaclass=ABCMeta):
    """
    BasePlatform
    """

    @abstractmethod
    def get_display_content(self, url, params=None):
        ...
    
    def get_headers(self):
        return {"User-Agent": useragent_random()}