from bs4 import BeautifulSoup
from gevent.pool import Pool
import re
import requests

from movieSource.platforms import BasePlatform


class LOLHeavenPlatform(BasePlatform):
    name = 'LOLHeaven'
    chinese_name = 'LOL电影天堂'
    
    def __init__(self, parent=None):
        self.__pool = Pool(8)
        self.__search_domain = 'https://www.993dy.com'
        self.__search_url = 'https://www.993dy.com/index.php'
        self.__movie_url_list = []
        self.__detail_url_list = []
    
    def get_display_content(self, url=None, params=None):
        hrefs = self.__get_the_search_movie_urls({"keyword":params['keyword'],"remain":True})
        _ = [self.__parse_search_url(href) for href in hrefs]
        self.__pool.map(self.__get_download_url, self.__detail_url_list)
        self.__pool.join()
        return self.__movie_url_list

    
    def __get_the_search_movie_urls(self, kw):
        """
            **kw:
                keyword: if is set,default search url
                url: if not set，default search url
                remain: if not set, not return remain hrefs
                submit: when url is not set worked,default '搜索影片'
        """
        url = kw.get("url", None)
        if not url:
            url = f'{self.__search_url}?m=vod-search&wd={kw.get("keyword").decode("gb2312")}&submit={kw.get("submit","搜索影片")}'

        html = None
        resp = requests.get(url, headers=self.get_headers())
        html = resp.text
        self.__parse_search_html(html)

        if kw.get("remain", None):
            return self.__get_remain_hrefs(html)
    
    def __parse_search_url(self, url):
        resp = requests.get(url, headers=self.get_headers())
        return self.__parse_search_html(resp.text)

    def __parse_search_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find("ul", class_='img-list')
        for li in ul.find_all('li'):
            a = li.find('a')
            href = f'{self.__search_domain}{a["href"]}'
            self.__detail_url_list.append(href)

    def __get_remain_hrefs(self, html):
        soup = BeautifulSoup(html,'html.parser')
        remain_pages_a = soup.find_all('a',class_='pagelink_b')
        remain_hrefs = [f'{self.__search_domain}{a["href"]}' for a in remain_pages_a if a["href"]]
        return remain_hrefs
        
    
    def __get_download_url(self, url):
        resp = requests.get(url, headers=self.get_headers())
        resp.encoding = "utf8"
        pattern = re.compile(r"\$(http:.+?)#")
        all_download_url = pattern.findall(resp.text)
        try:
            self.__movie_url_list.extend(all_download_url)
        except:
            pass


if __name__ == '__main__':
    lol = LOLHeavenPlatform()
    print(lol.get_display_content(params={"keyword":"功夫"}))

    