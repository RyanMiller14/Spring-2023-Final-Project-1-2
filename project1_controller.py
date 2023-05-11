from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from pathlib import Path
from project1_view import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Controller(QMainWindow, Ui_mainWindow):

    MIN_VOLUME = 0
    MAX_VOLUME = 100
    MIN_CHANNEL = 1
    MAX_CHANNEL = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.__status = False
        self.__muted = False
        self.__volume = Controller.MAX_VOLUME
        self.__channel = Controller.MIN_CHANNEL

        self.button_power.clicked.connect(lambda: self.power())
        self.button_volume_up.clicked.connect(lambda: self.volume_up())
        self.button_volume_down.clicked.connect(lambda: self.volume_down())
        self.button_mute.clicked.connect(lambda: self.mute())
        self.button_channel_up.clicked.connect(lambda: self.channel_up())
        self.button_channel_down.clicked.connect(lambda: self.channel_down())
        self.button_channel_list.clicked.connect(lambda: self.channel_list())
        self.numpad_0.clicked.connect(lambda: self.numpad_pressed(0))
        self.numpad_1.clicked.connect(lambda: self.numpad_pressed(1))
        self.numpad_2.clicked.connect(lambda: self.numpad_pressed(2))
        self.numpad_3.clicked.connect(lambda: self.numpad_pressed(3))
        self.numpad_4.clicked.connect(lambda: self.numpad_pressed(4))
        self.numpad_5.clicked.connect(lambda: self.numpad_pressed(5))
        self.numpad_6.clicked.connect(lambda: self.numpad_pressed(6))
        self.numpad_7.clicked.connect(lambda: self.numpad_pressed(7))
        self.numpad_8.clicked.connect(lambda: self.numpad_pressed(8))
        self.numpad_9.clicked.connect(lambda: self.numpad_pressed(9))


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        widget.setGeometry(QtCore.QRect(10, 0, 390, 210))
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)

    def power(self):
        self.__status = not self.__status
        if self.__status == True:
            Controller.PWR_STATUS = 'ON'
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(str((Path(__file__).with_name(f'channel{self.__channel}.wmv')).absolute()))))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
        elif self.__status == False:
            Controller.PWR_STATUS = 'OFF'
            self.mediaPlayer.stop()
            self.label_info.setText('')
        self.label_power.setText(f'Power = {Controller.PWR_STATUS}')

    def volume_up(self):
        if self.__status == True:
            self.mediaPlayer.setMuted(False)
            self.__volume += 20
            self.mediaPlayer.setVolume(self.__volume)
            if self.__volume > Controller.MAX_VOLUME:
                self.__volume = Controller.MAX_VOLUME
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def volume_down(self):
        if self.__status == True:
            self.mediaPlayer.setMuted(False)
            self.__volume -= 20
            self.mediaPlayer.setVolume(self.__volume)
            if self.__volume < Controller.MIN_VOLUME:
                self.__volume = Controller.MIN_VOLUME
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def mute(self):
        if self.__status == True and self.mediaPlayer.isMuted() == False:
            self.mediaPlayer.setMuted(True)
            self.mediaPlayer.setVolume(0)
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
        elif self.__status == True and self.mediaPlayer.isMuted() == True:
            self.mediaPlayer.setMuted(False)
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def channel_up(self):
        if self.__status == True:
            self.__channel += 1
            if self.__channel > Controller.MAX_CHANNEL:
                self.__channel = Controller.MIN_CHANNEL
            self.mediaPlayer.setMedia(QMediaContent(
                QUrl.fromLocalFile(str((Path(__file__).with_name(f'channel{self.__channel}.wmv')).absolute()))))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def channel_down(self):
        if self.__status == True:
            self.__channel -= 1
            if self.__channel < Controller.MIN_CHANNEL:
                self.__channel = Controller.MAX_CHANNEL
            self.mediaPlayer.setMedia(QMediaContent(
                QUrl.fromLocalFile(str((Path(__file__).with_name(f'channel{self.__channel}.wmv')).absolute()))))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def numpad_pressed(self, numpad_num):
        if self.__status == True:
            if numpad_num in range(Controller.MIN_CHANNEL, Controller.MAX_CHANNEL + 1):
                if self.__channel != numpad_num:
                    self.__channel = numpad_num
                    self.mediaPlayer.setMedia(QMediaContent(
                        QUrl.fromLocalFile(str((Path(__file__).with_name(f'channel{numpad_num}.wmv')).absolute()))))
                    self.mediaPlayer.play()
                    self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
            else:
                self.label_info.setText(f'Channel {numpad_num} not currently available')
    def channel_list(self):
        if self.__status == True:
            self.label_info.setText('Channels Available: 1-5')


