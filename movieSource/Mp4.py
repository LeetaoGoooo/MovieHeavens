# -*- encoding:utf-8 -*-
import requests
import re
import urllib
from multiprocessing.dummy import Pool as ThreadPool
from SearchMovieParent import SearchMovieParent
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Mp4(SearchMovieParent):
        '''
            Mp4吧
        '''
	def __init__(self,parent=None):
		self.__pool = ThreadPool(8)
		self.__domain = 'http://www.mp4ba.com/'
		self.__searchUrl = "http://www.mp4ba.com/search.php"
		self.__params = {"keyword":"leetao"}
        
	def __searchMovieResults(self,url=None,params=None):
		if url is not None:
			if params is not None:
				params = urllib.urlencode(params)
				tempResults = requests.get(url,params=params)
			else:
				tempResults = requests.get(url)
		else:
			if params is not None:
				tempResults = requests.get(self.__searchUrl,params=params)
			else:
				tempResults = requests.get(url)
		return tempResults.text
    
	def __getMovieDetailsPage(self,searchResults):
		# self.__writeResults(searchResults,'./results.txt')
		searchResults = searchResults.decode('gbk', 'ignore').encode('utf-8');
		downPageUrlPattern = re.compile('<a\sstyle="color:green;font-weight:bold;"\shref="(.*)"\starget="_blank">')
		downPageUrlList = downPageUrlPattern.findall(searchResults)
		return downPageUrlList

	def __getDownUrlList(self,downPageUrlList):
		downUrlList = []
		downpageContentUrlList = [(self.__domain + url) for url in downPageUrlList]
		downUrlList.append(self.__pool.map(self.__getDownLoadUrl,self.__pool.map(self.__searchMovieResults,downpageContentUrlList)))
		self.__pool.close()
		self.__pool.join()
		return downUrlList

	def __writeResults(self,dataResults,writeTargetFile):
		output = open(writeTargetFile,'w+')
		output.writelines(dataResults)
		output.close()
	
	def __getDownLoadUrl(self,downpageContent):
		downpageContent = downpageContent.decode('gbk', 'ignore').encode('utf-8');
		btnDownLoadUrlPattern = re.compile('<a\sid="magnet"\shref="(.*)">')
		btnDownLoadPartUrlList = btnDownLoadUrlPattern.findall(downpageContent)
		btnDownLoadUrlList = [(self.__domain + url) for url in btnDownLoadPartUrlList]
		if len(btnDownLoadUrlList) > 0:
			return 	btnDownLoadUrlList[0]
		else:
			return 'unknown bt'
	
	def getDisplayContent(self,url,params):
		searchMovieResults = self.__searchMovieResults(url,params)
		MovieDetailsPage = self.__getMovieDetailsPage(searchMovieResults)
		btDownLoadUrlList = self.__getDownUrlList(MovieDetailsPage)
		if len(btDownLoadUrlList[0]) > 0:
			return btDownLoadUrlList[0]
		else:
			return ['Not Found']


if __name__ == '__main__':
    url = 'http://www.mp4ba.com/search.php'
    params = {}
    params['keyword'] = '功夫熊猫'
    results = Mp4().getDisplayContent(url,params)
    print (',').join(results)