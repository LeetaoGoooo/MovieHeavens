#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable = line-too-long
"""
    @FIle:BtHeaven.py
    
    ~~~~~~~~~~~
    :copyright: (c) 2020 by the Niyuhang.
    :license: BSD, see LICENSE for more details.
"""
# -*- encoding:utf-8 -*-
import requests
import re
import urllib
import sys
from urllib import parse
from lxml import etree
from gevent.pool import Pool

from movieSource.platforms import BasePlatform


class BtHeavenPlatform(BasePlatform):
    name = "BtHeaven"
    chinese_name = "Bt天堂"

    """
    1. 根据关键词获取到所有的电影detail url
    2. 对于url进行解析获取到对应的下载地址
    """

    __slots__ = ['__pool',
                 '__all_page_details_url_list',
                 '__search_url',
                 '__search_domain',
                 '__download_domain'
                 ]

    def __init__(self, parent=None):
        self.__pool = Pool(8)
        self.__all_page_details_url_list = []
        self.__search_url = "https://www.bt-tt.com/e/search/index.php"
        self.__search_domain = 'http://s.ygdy8.com'
        self.__download_domain = 'https://www.bt-tt.com/'

    def _get_the_search_movie_urls(self, keyword):
        """
        获取关键词搜索的所有电影的url
        :param keyword:
        :return:
        """
        payload = {
            "show": "title",
            "keyboard": keyword
        }
        search_movie_results = requests.post(
            self.__search_url, data=payload, headers=self.get_headers())
        search_movie_results.encoding = "gb2312"
        html = search_movie_results.text
        return self.__parse_the_search_html(html)

    def __parse_the_search_html(self, html):
        urls = []
        html_selector = etree.HTML(html)
        details = html_selector.xpath("//div[@id='list']/dl")
        for detail in details:
            relative_urls = detail.xpath("dt/a/@href")
            if relative_urls:
                relative_url = relative_urls[0]
                urls.append(parse.urljoin(self.__download_domain, relative_url))
        return urls

    def _get_download_url(self, movie_detail_url):
        print("search", movie_detail_url)
        movie_detail_results = requests.get(
            movie_detail_url, headers=self.get_headers())
        html = movie_detail_results.text
        return self.__parse_the_detail_html(html)

    @staticmethod
    def __parse_the_detail_html(html):
        html_selector = etree.HTML(html)
        download_urls = html_selector.xpath("//a[contains(@href, 'magnet:')]/@href")
        return download_urls or []

    def get_display_content(self, url=None, params=None):
        url_list = self._get_the_search_movie_urls(keyword=params["keyword"])
        if len(url_list) == 0:
            return ['Not Found']
        else:
            movie_list = []
            all_download_urls = self.__pool.map(self._get_download_url, url_list)
            self.__pool.join()
            _ = [movie_list.extend(download_urls) for download_urls in all_download_urls]
            return movie_list


if __name__ == '__main__':
    res = BtHeavenPlatform().get_display_content(params={"keyword": "日记"})
    print(res)
