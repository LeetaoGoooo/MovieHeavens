# -*- encoding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QListWidget, QGridLayout, QComboBox, QMessageBox, QApplication, QMenuBar, QAction, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, QThread, QObject
from PyQt5.QtGui import QIcon, QPixmap, QImage
from movieSource.MovieHeaven import MovieHeaven


class ImageWindow(QMainWindow):
    def __init__(self, resources, title):
        super(ImageWindow, self).__init__()
        self.setWindowTitle(title)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        image = QImage(resources)
        pixmap = QPixmap(resources)
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.resize(pixmap.width(), pixmap.height())
        layout.addWidget(image_label)


class LayoutDialog(QMainWindow):
    __slots__ = ['word', 'movie_name_label', 'movie_name_line_edit', 'movie_source_label', 'movie_source_combobox',
                 'search_push_button', 'tip_label', 'search_content_label', 'search_content_text_list']

    def __init__(self):
        super().__init__()
        self.left = 300
        self.top = 300
        self.width = 400
        self.height = 450

        self.work = WorkThread()
        self.init_widgets().init_layout().init_event()

    def init_widgets(self):
        self.setWindowTitle(self.tr("Search Movies"))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.movie_name_label = QLabel(self.tr("电影名称:"))
        self.movie_name_line_edit = QLineEdit()

        self.movie_source_label = QLabel(self.tr("选择片源:"))
        self.movie_source_combobox = QComboBox()
        self.movie_source_combobox.addItem(self.tr('电影天堂'))

        self.search_push_button = QPushButton(self.tr("查询"))

        self.tip_label = QLabel(self.tr("未开始查询..."))
        self.search_content_label = QLabel(self.tr("查询内容:"))
        self.search_content_text_list = QListWidget()

        self.menu_bar = self.menuBar()

        return self

    def init_layout(self):
        top_layout = QGridLayout()
        top_layout.addWidget(self.movie_name_label, 0, 0)
        top_layout.addWidget(self.movie_name_line_edit, 0, 1)
        top_layout.addWidget(self.movie_source_label, 0, 2)
        top_layout.addWidget(self.movie_source_combobox, 0, 3)
        top_layout.addWidget(self.search_push_button, 0, 4)
        top_layout.addWidget(self.tip_label, 3, 1)
        top_layout.addWidget(self.search_content_label, 3, 0)
        top_layout.addWidget(self.search_content_text_list, 4, 0, 2, 5)

        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(top_layout)

        self.reward_window = ImageWindow('resources/wechat_reward.jpg', '赞赏')
        self.watch_window = ImageWindow('resources/watch_wechat.jpg', '关注')

        return self

    def init_event(self):
        self.search_push_button.clicked.connect(self.search)
        self.search_content_text_list.itemClicked.connect(self.copy_text)

        reward_action = QAction('赞赏', self)
        reward_action.setIcon(QIcon('resources/reward.png'),)
        reward_action.triggered.connect(self.reward)

        watch_action = QAction('关注', self)
        watch_action.setIcon(QIcon('resources/watch.png'),)
        watch_action.triggered.connect(self.watch_wechat)

        reward_menu = self.menu_bar.addMenu('支持作者')
        reward_menu.addAction(reward_action)
        reward_menu.addAction(watch_action)

    def reward(self):
        self.reward_window.show()

    def watch_wechat(self):
        self.watch_window.show()

    def search(self):
        self.tip_label.setText(self.tr("正在查询请稍后..."))
        movie_name = self.movie_name_line_edit.text()
        if movie_name:
            self.work.render(movie_name, self.movie_source_combobox,
                             self.tip_label, self.search_content_text_list)
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
        movies, url, params = None, None, {
            "kwtype": "0", "searchtype": "title"}
        select_source = self.movie_source_combobox.currentText()
        if select_source == self.tr('电影天堂'):
            movies = MovieHeaven()
            url = "http://s.dydytt.net/plus/search.php"
            params["keyword"] = movie_name.encode('gb2312')
        return movies, url, params

    def run(self):
        search_movies, url, params = self.get_select_movie_source(
            self.movie_name)
        try:
            self.movies_list = search_movies.get_display_content(url, params)
        except Exception as e:
            self.movies_list.append(self.tr("过于频繁的访问"))
        finally:
            self.search_content_text_list.clear()
            self.search_content_text_list.addItems(self.movies_list)
            self.tip_label.setText(self.tr("查询结束"))


app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()
