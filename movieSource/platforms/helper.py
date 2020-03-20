#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:helper.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2017 by the eigen.
    :license: BSD, see LICENSE for more details.
"""

import importlib
import os
import re
import logging

from os import path

from movieSource.const import PLATFORM_MODULE_PATH, EXCLUDE_MODULE_NAME

logger = logging.getLogger(__name__)


def import_the_platform(name):
    try:
        module = importlib.import_module("{}.{}".format(PLATFORM_MODULE_PATH, name))
        platform = getattr(module, "{}Platform".format(name))
        return platform
    except Exception as e:
        logger.error(e)


def get_all_platforms():
    """
    :return: [Object<Platform>]
    """
    res = []
    platform_dir_path = path.dirname(path.abspath(__file__))
    files = os.listdir(platform_dir_path)
    # 加载所有platform
    pattern = re.compile(r"^([a-zA-Z]+)\.py$")
    for file_name in files:
        search_module_name = pattern.match(file_name)
        if search_module_name:
            module_name = search_module_name.groups()[0]
            if module_name == EXCLUDE_MODULE_NAME:
                continue
            logger.info("get module name, {}".format(module_name))
            platform = import_the_platform(module_name)
            res.append(platform) if platform else None
    return res


def get_all_platform_names():
    all_platforms = get_all_platforms()
    return [{"name": platform.name, "chinese_name": platform.chinese_name}
            for platform in all_platforms]


if __name__ == '__main__':
    get_all_platforms()