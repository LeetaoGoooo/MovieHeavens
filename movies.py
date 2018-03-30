# -*- encoding:utf-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from movieSource.MovieHeaven import MovieHeaven
import helpUI

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class LayoutDialog(QDialog, helpUI.Ui_Dialog):
    __slots__ = ['word', 'movie_name_label', 'movie_name_line_edit', 'movie_source_label', 'movie_source_combobox',
                 'search_push_button', 'tip_label', 'search_content_label', 'search_content_text_list']

    def __init__(self, parent=None):
        super(LayoutDialog, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkThread()

        self.setWindowTitle(self.tr("Search Movies"))
        self.setWindowIcon(QIcon('./searchMovies.ico'))

        self.movie_name_label = QLabel(self.tr("电影名称:"))
        self.movie_name_line_edit = QLineEdit()

        self.movie_source_label = QLabel(self.tr("选择片源:"))
        self.movie_source_combobox = QComboBox()
        self.movie_source_combobox.addItem(self.tr('电影天堂'))

        self.search_push_button = QPushButton(self.tr("查询"))

        self.tip_label = QLabel(self.tr("未开始查询..."))
        self.search_content_label = QLabel(self.tr("查询内容:"))
        self.search_content_text_list = QListWidget()

        top_layout = QGridLayout()
        top_layout.addWidget(self.movie_name_label, 0, 0)
        top_layout.addWidget(self.movie_name_line_edit, 0, 1)
        top_layout.addWidget(self.movie_source_label, 0, 2)
        top_layout.addWidget(self.movie_source_combobox, 0, 3)
        top_layout.addWidget(self.search_push_button, 0, 4)
        top_layout.addWidget(self.tip_label, 3, 1)
        top_layout.addWidget(self.search_content_label, 3, 0)
        top_layout.addWidget(self.search_content_text_list, 4, 0, 2, 5)

        self.setLayout(top_layout)
        self.connect(self.search_push_button, SIGNAL("clicked()"), self.search)
        self.search_content_text_list.itemClicked.connect(self.copy_text)

    def search(self):
        self.tip_label.setText(self.tr("正在查询请稍后..."))
        movie_name = self.movie_name_line_edit.text()
        if movie_name:
            self.work.render(movie_name, self.movie_source_combobox, self.tip_label, self.search_content_text_list)
        else:
            self.critical("请输入电影名称!")

    def critical(self, message):
        """
        when the movieName is None,
        remind users
        """
        QMessageBox.critical(self, self.tr("致命错误"),
                             self.tr(message))

    def copy_text(self):
        copied_text = self.search_content_text_list.currentItem().text()
        QApplication.clipboard().clear()
        QApplication.clipboard().setText(copied_text)
        self.slot_information()

    def slot_information(self):
        QMessageBox.information(self, "Success!", self.tr("成功将内容复制到剪贴板上!"))


class WorkThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def render(self, movie_name, movie_source_combobox, tip_label, search_content_text_list):
        self.movies_list = []
        self.movie_source_combobox = movie_source_combobox
        self.movie_name = movie_name
        self.tip_label = tip_label
        self.search_content_text_list = search_content_text_list
        self.start()

    def get_select_movie_source(self, movie_name):
        """
        according to the value of the QComboBox,
        generate the right class of movie search
        """
        movies, url, params = None, None, {"kwtype": "0", "searchtype": "title"}
        select_source = self.movie_source_combobox.currentText()
        if select_source == self.tr('电影天堂'):
            movies = MovieHeaven()
            url = "http://s.dydytt.net/plus/search.php"
            params["keyword"] = movie_name
        return movies, url, params

    def run(self):
        search_movies, url, params = self.get_select_movie_source(self.movie_name)
        try:
            self.movies_list = search_movies.get_display_content(url, params)
        except Exception as e:
            print(e)
            self.movies_list.append(self.tr("过于频繁的访问"))
        finally:
            self.search_content_text_list.clear()
            self.search_content_text_list.addItems(self.movies_list)
            self.tip_label.setText(self.tr("查询结束"))


app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()
