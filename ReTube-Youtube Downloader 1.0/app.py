import sys
import pytube
import os
import requests
import wget
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QComboBox, QFormLayout, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QFont

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("ReTube - Youtube Downloader")
        self.setWindowIcon(QtGui.QIcon('images/retube.ico'))
        self.setStyleSheet("background: #fff;")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        #membuat label judul
        header_label = QLabel("Youtube Downloader")
        header_label.setFont(QFont("Poppins", 25))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #membuat line edit link
        self.link = QLineEdit()
        self.link.setPlaceholderText("Paste youtube link here")
        self.link.setFont(QFont("Poppins", 12))
        self.link.setStyleSheet('''
        *{
            background: '#fddfe0';
            color: '#ed1c24';
            padding: 20px 30px;
        }
        '''
        )

        #membuat tombol start
        self.start = QPushButton("Start")
        self.start.clicked.connect(self.show_data_proccess)
        self.start.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.start.setFont(QFont("Poppins", 14))
        self.start.setStyleSheet(
            '''
            *{
                color: '#fff';
                background: '#ed1c24';
                padding: 18px 30px;
                margin: 10px 5px;
            }
            *:hover{
                background: '#07060a';
            }
            '''
        )

        #membuat section untuk thumbnail
        self.thumbnail = QLabel()
        pixmap = QPixmap("images/thumbnail.jpg")
        pixmap_scaled = pixmap.scaled(480,270)
        self.thumbnail.setPixmap(pixmap_scaled)
        self.thumbnail.setScaledContents(True)

        #membuat tombol download
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_vid)
        self.download_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.download_button.setFont(QFont("Poppins", 14))
        self.download_button.setStyleSheet(
            '''
            *{
                color: '#fff';
                background: '#1caf7e';
                padding: 10px 60px;
                margin: 5px 15px;
            }
            *:hover{
                background: '#ed1c24';
            }
            '''
        )

        #membuat tombol download thumbnail
        self.download_thumb = QPushButton("Download Thumbnail")
        self.download_thumb.clicked.connect(self.download_thumbnail)
        self.download_thumb.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.download_thumb.setFont(QFont("Poppins", 9))
        self.download_thumb.setStyleSheet(
            '''
            *{
                color: '#fff';
                background: '#00a2e8';
                padding: 5px 10px;
                margin: 5px 15px;
            }
            *:hover{
                background: '#999999';
            }
            '''
        )

        #membuat combo box pilihan resolusi
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["1080p.", "720p.", "480p.", "360p.", "m4a. (audio)"])
        self.resolution_combo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.resolution_combo.setFont(QFont("Poppins", 12))
        self.resolution_combo.setStyleSheet(
            '''
            *{
                color: 'black';
                background: '#eeeded';
                padding: 10px 5px;
                margin: 5px 5px;
            }
            '''
        )

        #membuat label untuk deskripsi video
        self.title = QLabel("Title : ")
        self.title.setWordWrap(True)
        self.title.setStyleSheet(
            '''
            *{
                font-family: 'poppins';
                font-size : 18px;
                color: 'black';
                margin: 5px;
            }
            '''
        )
        self.author = QLabel("Author : ")
        self.author.setStyleSheet(
            '''
            *{
                font-family: 'poppins';
                font-size : 16px;
                color: '#9fa5aa';
                margin: 5px;
            }
            '''
        )
        self.duration = QLabel("Duration : ")
        self.duration.setStyleSheet(
            '''
            *{
                font-family: 'poppins';
                font-size : 13px;
                color: '#adadad';
                margin: 5px 5px;
            }
            '''
        )

        #membut line pembatas deskripsi video
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet(
            '''
            *{
                color: '#adadad';
                margin: 30px 0px;
            }
            '''
        )

        self.linex = QFrame()
        self.linex.setFrameShape(QFrame.HLine)
        self.linex.setFrameShadow(QFrame.Sunken)
        self.linex.setStyleSheet(
            '''
            *{
                color: '#adadad';
                margin: 30px 0px;
            }
            '''
        )

        #membuat status download dan show data
        self.status = QLabel("DOWNLOAD STATUS")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setStyleSheet(
            '''
            *{
                font-family: 'poppins';
                font-size : 17px;
                color: '#adadad';
                margin: 5px 5px;
                margin-top: 10px;
                padding : 2px 10px;
                background-color: '#fff';
                border: 1px solid '#adadad';
            }
            '''
        )

        #membuat box untuk judul
        header_box = QHBoxLayout()
        header_box.addWidget(header_label)

        #membuat box untuk line edit dan start
        second_box = QHBoxLayout()
        second_box.addWidget(self.link)
        second_box.addWidget(self.start)

        #membuat box untuk download button
        self.download_box = QVBoxLayout()
        self.download_box.addWidget(self.download_button)
        self.download_box.addWidget(self.download_thumb)

        #membuat grid untuk download,thumbnail,dan resolusi
        grid = QGridLayout()
        grid.addLayout(self.download_box, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.thumbnail, 0, 0, 0, 1)
        grid.addWidget(self.resolution_combo, 0, 2, alignment=Qt.AlignmentFlag.AlignTop)

        #membuat box untuk deskripsi video
        self.description_box = QVBoxLayout()
        self.description_box.addWidget(self.line)
        self.description_box.addWidget(self.title)
        self.description_box.addWidget(self.author)
        self.description_box.addWidget(self.duration)
        self.description_box.addWidget(self.linex)

        #membuat box untuk status download
        self.status_box = QHBoxLayout()
        self.status_box.addWidget(self.status)

        #membuat layout untuk window
        main_layout = QFormLayout()
        main_layout.addRow(header_box)
        main_layout.addRow(second_box)
        main_layout.addRow(grid)
        main_layout.addRow(self.description_box)
        main_layout.addRow(self.status_box)
        self.setLayout(main_layout)

    def show_data_proccess(self):
        link = self.link.text()
        if link != "":
            self.status.setText("SHOWING VIDEO DATA")

        self.show_data()

    def show_data(self):
        link = self.link.text()
        if link != "":
            yt = pytube.YouTube(link)

        #menampilkan title video

        self.title.setText("Title : " + yt.title)

        #menampilkan author video

        self.author.setText("Author : " + yt.author)

        #menampilkan durasi video

        duration = yt.length
        minute = duration // 60
        seconds = duration % 60
        self.duration.setText("Duration : " + str(minute) + ":" + str(seconds))

        #menampilkan thumbnail video
        thumb = yt.thumbnail_url
        response = requests.get(thumb)
        image = QPixmap()
        image.loadFromData(response.content)
        pixmap_scaled = image.scaled(480, 270)
        self.thumbnail.setPixmap(pixmap_scaled)
        self.thumbnail.setScaledContents(True)

    def download_vid(self):
        link = self.link.text()
        if link != "":
            yt = pytube.YouTube(link)

            # split pilihan resolusi
            resolution = self.resolution_combo.currentText()
            reso = resolution.split(".")[0]

            # lokasi file di folder download users
            home = os.path.expanduser('~')
            location = os.path.join(home, 'Downloads')

            # download resolusi untuk video (mp4)
            if reso != "m4a":
                stream = yt.streams.filter(res=reso, file_extension='mp4')
                video = stream.first()
                video.download(str(location))
                self.status.setText("video was saved into " + location)

            # download resolusi untuk audio (m4a)
            else:
                audio = yt.streams.get_by_itag(140).download(str(location))
                # ubah jenis file dari mp4 menjadi m4a
                new_name = os.path.splitext(audio)
                os.rename(audio, new_name[0] + '.m4a')
                self.status.setText("audio was saved into " + location)

    def download_thumbnail(self):
        link = self.link.text()
        if link != "":
            # lokasi file di folder download users
            home = os.path.expanduser('~')
            location = os.path.join(home, 'Downloads')

            #inisiasi thumbnail youtube
            thumb_show = pytube.YouTube(link).thumbnail_url

            #download dengan wget
            wget.download(thumb_show, location)
            self.status.setText("thumbnail was saved to " + location)



if __name__ == '__main__':
 app = QApplication(sys.argv)
 window = MainWindow()
 sys.exit(app.exec())