# -*- encoding:utf-8 -*-
import requests
import re
import urllib
from movieSource.fake_user_agent import useragent_random
from multiprocessing.dummy import Pool as ThreadPool
import sys


class MovieHeaven:
    __slots__ = ['__pool', '__all_page_details_url_list', '__search_url', '__search_domain', '__download_domain',
                 '__params']

    def __init__(self, parent=None):
        self.__pool = ThreadPool(8)
        self.__all_page_details_url_list = []
        self.__search_url = "http://s.dydytt.net/plus/s0.php"
        self.__search_domain = 'http://s.ygdy8.com'
        self.__download_domain = 'http://www.ygdy8.com'
        self.__params = {"typeid": "1",
                        "keyword": "leetao"}

    def __get_headers(self):
        return {"User-Agent": useragent_random()}

    def __search_movie_results(self, url=None, params=None):
        if url is None:
            url = self.__search_url

        temp_results = requests.get(
            url, params=params, headers=self.__get_headers())
        temp_results.encoding = 'gb2312'
        return temp_results.text

    def __get_movies_detail_page(self, searchResults):
        """
        get the detailPage's url of movies by using regx
        """
        pattern = re.compile(
            r"<td\s+width='\d+%'><b><a\s+href='(.*\.html)'\s*>")
        all_detai_pages = pattern.findall(searchResults)
        return all_detai_pages

    def __get_page_number_total(self, searchResults):
        """
        get the total number of pages
        """
        page_num_total_pattern = re.compile(
            r"<td\s+width='30'><a\s+href='.+PageNo=(\d+)'\s*>")
        page_num_total = page_num_total_pattern.findall(searchResults)
        if len(page_num_total) == 0:
            return -1
        else:
            return int(page_num_total[0])

    def __next_page_detail(self, search_results):
        """
        get the next page'url which lacks the pagenumber
        """
        next_page_pattern = re.compile(
            r"<td\s+width='30'><a href='(.*PageNo=)\d+'>")
        next_page_url = next_page_pattern.findall(search_results)
        return str(next_page_url[0])

    def __get_search_content_by_url(self, next_page_url, page_num_total):
        """
        get remain pages's url
        """
        for page_no in range(2, page_num_total + 1):
            if page_no is not None:
                url = self.__search_domain + next_page_url + str(page_no)
                res = self.__search_movie_results(url)
                return self.__get_movies_detail_page(res)

    def __get_movie_contents_url(self, url, params=None):
        """
        get the first page of searching results
        and  get the remain pages's results
        """
        first_page_results = self.__search_movie_results(url, params)
        first_page_resultsList = self.__get_movies_detail_page(
            first_page_results)

        # get the remain pages's results
        total_page_num = self.__get_page_number_total(first_page_results)
        if total_page_num > 0:
            next_page_url = self.__next_page_detail(first_page_results)
            remain_page_results_list = self.__get_search_content_by_url(
                next_page_url, total_page_num)
            self.__all_page_details_url_list.extend(remain_page_results_list)

        self.__all_page_details_url_list.extend(first_page_resultsList)
        return self.__all_page_details_url_list

    def __get_movie_down_url(self, down_page_url_list):
        results_list = []
        down_page_content_url_list = [
            (self.__download_domain + url) for url in down_page_url_list]
        for result_url_list in self.__pool.map(self.__get_down_page_content_url, self.__pool.map(self.__search_movie_results, down_page_content_url_list)):
            if len(result_url_list) > 0:
                results_list += result_url_list

        self.__pool.close()
        self.__pool.join()
        return results_list

    def __get_down_page_content_url(self, down_page_content):
        download_url_list = []
        ftp_down_pattern = re.compile(r'<td.+><a\s+href="(.+)"\s*>')
        ftp_url_list = ftp_down_pattern.findall(down_page_content)
        if len(ftp_url_list) > 0:
            download_url_list.append(ftp_url_list[0])

        magnet_down_pattern = re.compile(
            r'<a\s+href="(magnet:\?xt=.+)"><strong>')
        magnet_url_list = magnet_down_pattern.findall(down_page_content)
        if len(magnet_url_list) > 0:
            download_url_list.append(magnet_url_list[0].replace("amp;", ""))

        return download_url_list

    def get_display_content(self, url, params=None):
        url_list = self.__get_movie_contents_url(url, params)
        if len(url_list) == 0:
            return ['Not Found']
        else:
            all_download_url_list = self.__get_movie_down_url(url_list)
            movie_list = [
                url for url in all_download_url_list if url is not None and url[-3:] not in ['zip', 'rar', 'exe']]
            return movie_list
