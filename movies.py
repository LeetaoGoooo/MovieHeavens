# -*- encoding:utf-8 -*-
import requests
import sys
import re
import urllib
reload(sys)
sys.setdefaultencoding("utf-8")
from PyQt4.QtGui import *
from PyQt4.QtCore import *

"""
http://s.kujian.com/plus/search.php?kwtype=0&searchtype=title&keyword=
"""

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class LayoutDialog(QDialog):
	def __init__(self,parent=None):
		super(LayoutDialog,self).__init__(parent)
		self.searchUrl = "http://s.kujian.com/plus/search.php"

		self.setWindowTitle(self.tr("Search Movies"))

		self.movieNameLabel = QLabel(self.tr("电影名称:"))
		self.movieNameLineEdit = QLineEdit()

		self.searchPushButton = QPushButton(self.tr("查询"))

		self.searchContentLabel = QLabel(self.tr("Search Content"))
		self.searchContentTextList = QListWidget()

		topLayout = QGridLayout()
		topLayout.addWidget(self.movieNameLabel,0,0)
		topLayout.addWidget(self.movieNameLineEdit,0,1)
		topLayout.addWidget(self.searchPushButton,0,2)
		topLayout.addWidget(self.searchContentLabel,1,0)
		topLayout.addWidget(self.searchContentTextList,2,1)

		self.setLayout(topLayout)
		self.connect(self.searchPushButton,SIGNAL("clicked()"),self.search)

	def search(self):
			self.SearchMovies = SearchMovies()
			movieName = self.movieNameLineEdit.text()
			movieName =  unicode(movieName.toUtf8(),'utf8','ignore')
			movieName = movieName.encode('gb2312')
			params = {"kwtype":"0","searchtype":"title"}
			params["keyword"] = movieName
			moviesList = self.SearchMovies.getDisplayContent(self.searchUrl,params)
			self.searchContentTextList.addItems(moviesList)



class SearchMovies:
		"""
		对抓取页面进行分析
		爬虫主体	
		"""	
		def __init__(self,parent=None):
			self.__AllPageDetailsUrlList = []
			self.__searchUrl = "http://s.kujian.com/plus/search.php"
			self.__searchDomain = 'http://s.kujian.com'
			self.__downloadDomain = 'http://www.ygdy8.com'

		def __searchMoviesResults(self,url=None,params=None):
			"""
			电影天堂关键字的gb2312格式，然后再url编码 
			"""
			if url is not None:
				if params is not None:
					params = urllib.urlencode(params)
					tempResults = requests.get(url,params=params)
				else:
					tempResults = requests.get(url)
			else:
				tempResults = requests.get(self.__searchUrl,params)
			tempResults.encoding = 'gb2312'
			return tempResults.text

		def __writeResults(self,dataResults,writeTargetFile):
			output = open(writeTargetFile,'w+')
			output.writelines(dataResults)
			output.close()

		def __getMoviesDetailPage(self,searchResults):
			"""
			get the detailPage's url of movies by using regx
			"""
			pattern = re.compile(r"<td\s+width='\d+%'><b><a\s+href='(.*\.html)'\s*>")
			allDetaiPages = pattern.findall(searchResults)
			return allDetaiPages

		def __getPageNumTotal(self,searchResults):
			"""
			get the total number of pages
			"""
			PageNumTotalPattern = re.compile(r"<td\s+width='30'><a\s+href='.+PageNo=(\d+)'\s*>")
			PageNumTotal = PageNumTotalPattern.findall(searchResults)
			if len(PageNumTotal) == 0:
				return -1
			else:
				return int(PageNumTotal[0])


		def __nextPageDetail(self,searchResults):
			"""
			get the next page'url which lacks the pagenumber
			"""
			nextPagePattern = re.compile(r"<td\s+width='30'><a href='(.*PageNo=)\d+'>")
			nextPageUrl = nextPagePattern.findall(searchResults)
			return str(nextPageUrl[0])


		def __getSearchContentByUrl(self,nextPageUrl,pagenumtotal):
			"""
			get remain pages's url
			"""
			for pageno in range(2,pagenumtotal+1):
				if pageno is not None:
					url = self.__searchDomain + nextPageUrl + str(pageno)
					res = self.__searchMoviesResults(url)
					return self.__getMoviesDetailPage(res)

		def __testFind(self):
			readAll = open('data')
			try:
				all_the_text = readAll.read()
			finally:
				readAll.close()
			print('doing')
			#self.getMoviesDetailPage(all_the_text)
			self.nextPageDetail(all_the_text)
		

		def __getMovieContentsUrl(self,url,params=None):
			"""
			get the first page of searching results
			and  get the remain pages's results
			"""
			firstPageResults = self.__searchMoviesResults(url,params)
			firstPageResultsList = self.__getMoviesDetailPage(firstPageResults)
			#get the remain pages's results
			TotalPageNum = self.__getPageNumTotal(firstPageResults)
			if TotalPageNum > 0: 
				nextPageUrl = self.__nextPageDetail(firstPageResults)
				remainPageResultsList = self.__getSearchContentByUrl(nextPageUrl,TotalPageNum)
				self.__AllPageDetailsUrlList.extend(remainPageResultsList)

			self.__AllPageDetailsUrlList.extend(firstPageResultsList)
			return self.__AllPageDetailsUrlList


		def __getMovieDownUrl(self,downPageUrlList):
			resultsList = []
			for url in downPageUrlList:
				downPageContentUrl = self.__downloadDomain + str(url)
				downPageContent = self.__searchMoviesResults(downPageContentUrl)
				resultsList.append(self.__getDownPageContentUrl(downPageContent))
			return resultsList

		def __getDownPageContentUrl(self,downPageContent):
			downPattern = re.compile(r'<td.+><a\s+href="(.+)"\s*>')	
			ftpUrlList = downPattern.findall(downPageContent)
			#self.__writeResults(downPageContent,'downPageContent',)
			ftpUrl = ftpUrlList[0]
			return ftpUrl


		def getDisplayContent(self,url,params=None):
			urlList = self.__getMovieContentsUrl(url,params)
			if len(urlList) == 0:
				#print('Not Found')
				return ['Not Found']
			else:
				allDownLoadUrlList =  self.__getMovieDownUrl(urlList)
				#print allDownLoadUrlList
				return allDownLoadUrlList

app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()