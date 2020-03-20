#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long

from abc import abstractmethod, ABCMeta


class BasePlatform(metaclass=ABCMeta):
    """
    BasePlatform
    """

    @abstractmethod
    def get_display_content(self, url, params=None):
        ...
