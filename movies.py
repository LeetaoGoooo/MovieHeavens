# -*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from movieSource.MovieHeaven import SearchMovies

"""
http://s.kujian.com/plus/search.php?kwtype=0&searchtype=title&keyword=
fix a bug~~功夫熊猫搜索
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


app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()