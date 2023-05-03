from PyQt5.QtWidgets import *
from project1_view import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Controller(QMainWindow, Ui_mainWindow):

    PWR_STATUS = 'OFF'
    MIN_VOLUME = 0
    MAX_VOLUME = 10
    MIN_CHANNEL = 1
    MAX_CHANNEL = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.__status = False
        self.__muted = False
        self.__volume = Controller.MIN_VOLUME
        self.__channel = Controller.MIN_CHANNEL

        self.button_power.clicked.connect(lambda: self.power())
        self.button_volume_up.clicked.connect(lambda: self.volume_up())
        self.button_volume_down.clicked.connect(lambda: self.volume_down())
        self.button_mute.clicked.connect(lambda: self.mute())
        self.button_channel_up.clicked.connect(lambda: self.channel_up())
        self.button_channel_down.clicked.connect(lambda: self.channel_down())
        self.button_channel_list.clicked.connect(lambda: self.channel_list())


    def power(self):
        self.__status = not self.__status
        if self.__status == True:
            Controller.PWR_STATUS = 'ON'
        elif self.__status == False:
            Controller.PWR_STATUS = 'OFF'
        self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = {self.__volume}')

    def volume_up(self):
        self.__muted = False
        if self.__status == True:
            self.__volume += 1
            if self.__volume > Controller.MAX_VOLUME:
                self.__volume = Controller.MAX_VOLUME
            self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = {self.__volume}')

    def volume_down(self):
        self.__muted = False
        if self.__status == True:
            self.__volume -= 1
            if self.__volume < Controller.MIN_VOLUME:
                self.__volume = Controller.MIN_VOLUME
            self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = {self.__volume}')

    def mute(self):
        if self.__status == True:
            self.__muted = not self.__muted
            self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = 0')

    def channel_up(self):
        if self.__status == True:
            self.__channel += 1
            if self.__channel > Controller.MAX_CHANNEL:
                self.__channel = Controller.MIN_CHANNEL
            self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = {self.__volume}')

    def channel_down(self):
        if self.__status == True:
            self.__channel -= 1
            if self.__channel < Controller.MIN_CHANNEL:
                self.__channel = Controller.MAX_CHANNEL
            self.label_info.setText(f'Power = {Controller.PWR_STATUS}\nChannel = {self.__channel}\nVolume = {self.__volume}')

    def channel_list(self):
        if self.__status == True:
            self.label_info.setText('Available 1-10')


