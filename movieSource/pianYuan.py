# -*- encoding:utf-8 -*-
import requests
import re
import urllib
from multiprocessing.dummy import Pool as ThreadPool 
from SearchMovieParent import SearchMovieParent

class pianYuan(SearchMovieParent):
	"""
		the spider of pianyuan.net
	"""
	def __init__(self,parent=None):
		self.__pool = ThreadPool(8)
		self.__domain = "http://pianyuan.net"
		self.__searchUrl = "http://pianyuan.net/search"

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
		downPageUrlPattern = re.compile('<a\s+target="_blank"\s+href="(.*)"\s+class="ico ico_bt">')
		downPageUrlList = downPageUrlPattern.findall(searchResults)
		return downPageUrlList

	def __getDownUrlList(self,downPageUrlList):
		"""
		all items in downPageUrlList lacks the domain 
		"""
		downUrlList = []
		# for url in downPageUrlList:
		# 	completeUrl = self.__domain + str(url)
		# 	downpageContent = self.__searchMovieResults(completeUrl)
		# 	downUrlList.append(self.__getDownLoadUrl(downpageContent))
		#downpageContentUrlList = []
		downpageContentUrlList = [(self.__domain + url) for url in downPageUrlList]
		downUrlList.append(self.__pool.map(self.__getDownLoadUrl,self.__pool.map(self.__searchMovieResults,downpageContentUrlList)))
		self.__pool.close()
		self.__pool.join()
		return downUrlList

	def __getDownLoadUrl(self,downpageContent):
		btDownLoadUrlPattern = re.compile('</a>\s+<a\s+href="(.*)"\s+class="btn\s+btn-primary\s+btn-sm">')
		btDownLoadUrlList = btDownLoadUrlPattern.findall(downpageContent)
		if len(btDownLoadUrlList) > 0:
			return btDownLoadUrlList[0]
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