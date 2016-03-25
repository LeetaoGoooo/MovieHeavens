# -*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from movieSource.MovieHeaven import MovieHeaven
from movieSource.pianYuan import pianYuan
import time
"""
http://s.kujian.com/plus/search.php?kwtype=0&searchtype=title&keyword=
"""

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class LayoutDialog(QDialog):
	def __init__(self,parent=None):
		super(LayoutDialog,self).__init__(parent)
		self.setWindowTitle(self.tr("Search Movies"))
		self.setWindowIcon(QIcon('./searchMovies.ico'))
		self.movieNameLabel = QLabel(self.tr("电影名称:"))
		self.movieNameLineEdit = QLineEdit()

		self.movieSourceLabel = QLabel(self.tr("选择片源:"))
		self.movieSourceComboBox = QComboBox()
		self.movieSourceComboBox.addItem(self.tr('电影天堂'))
		self.movieSourceComboBox.addItem(self.tr('片源网'))

		self.searchPushButton = QPushButton(self.tr("查询"))

		self.searchContentLabel = QLabel(self.tr("查询内容:"))
		self.searchContentTextList = QListWidget()

		topLayout = QGridLayout()
		topLayout.addWidget(self.movieNameLabel,0,0)
		topLayout.addWidget(self.movieNameLineEdit,0,1)
		topLayout.addWidget(self.movieSourceLabel,0,2)
		topLayout.addWidget(self.movieSourceComboBox,0,3)
		topLayout.addWidget(self.searchPushButton,0,4)
		topLayout.addWidget(self.searchContentLabel,2,0)
		topLayout.addWidget(self.searchContentTextList,3,0,2,5)

		self.setLayout(topLayout)
		self.connect(self.searchPushButton,SIGNAL("clicked()"),self.search)
		self.searchContentTextList.itemClicked.connect(self.CopyText)

	def search(self):
			movieName = self.movieNameLineEdit.text()
			if movieName:
				SearchMovies,searchUrl,params = self.getSelectMovieSource(movieName)
				moviesList = SearchMovies.getDisplayContent(searchUrl,params)
				self.searchContentTextList.clear()
				self.searchContentTextList.addItems(moviesList)
			else:
				self.Critical()

	def CopyText(self):
		copytext = self.searchContentTextList.currentItem().text()
		QApplication.clipboard().clear()
		QApplication.clipboard().setText(copytext)
		self.slotInformation()

	def getSelectMovieSource(self,movieName):
		"""
		according to the value of the QComboBox,
		generate the right class of movie search
		"""
		selectSouce = self.movieSourceComboBox.currentText()
		if selectSouce == self.tr('电影天堂'):
			movieName =  unicode(movieName.toUtf8(),'utf8','ignore')
			movieName = movieName.encode('gb2312')
			Movies = MovieHeaven()
			Url = "http://s.kujian.com/plus/search.php"
			params = {"kwtype":"0","searchtype":"title"}
			params["keyword"] = movieName
		elif selectSouce == self.tr('片源网'):
			Movies = pianYuan()
			Url = "http://pianyuan.net/search"
			movieName =  unicode(movieName.toUtf8(),'utf8','ignore')
			params = {}
			params['q'] = movieName
		return Movies,Url,params
	
	def Critical(self):
		"""
		when the movieName is None,
		remain users

		"""
		QMessageBox.critical(self,self.tr("致命错误"),
		self.tr("请输入电影名称!"))

	def slotInformation(self):
		QMessageBox.information(self,"Success!",self.tr("成功将内容复制到剪贴板上!"))  
	
app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()