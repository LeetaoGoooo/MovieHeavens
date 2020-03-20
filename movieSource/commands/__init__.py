#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:__init__.py.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2017 by the eigen.
    :license: BSD, see LICENSE for more details.
"""
from abc import abstractmethod, ABCMeta


class Command(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class Invoker:

    def __init__(self, command):
        self._command = command

    @property
    def command(self):
        return self._command

    def run(self, *args, **kwargs):
        return self.command.execute(*args, **kwargs)