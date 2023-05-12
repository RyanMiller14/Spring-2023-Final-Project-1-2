from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from project1_view import *
import os
import sys

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Controller(QMainWindow, Ui_mainWindow):
    """
    A class that determines both volume and channel limit values, finds the path of the executable, and
    defines methods for buttons on the GUI.
    """
    MIN_VOLUME = 0
    MAX_VOLUME = 100
    MIN_CHANNEL = 1
    MAX_CHANNEL = 5

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    def __init__(self, *args, **kwargs) -> None:
        """
        Constructor to create initial state of the GUI controller.
        VideoWidget and mediaPlayer are created.
        Checks and handles button input.
        :param args: Collects all arguments from user input with the GUI.
        :param kwargs: Collects all key arguments from user input with the GUI.
        """
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
        self.mediaPlayer.error.connect(self.handleError)

    def handleError(self):
        self.label_error.setText("Error: " + self.mediaPlayer.errorString())

    def power(self) -> None:
        """
        Method that determines whether buttons have effect when pressed.
        Upon activation, mediaPlayer displays last known channel.
        Upon deactivation, mediaPlayer displays a blank/black screen.
        """
        channel = f'channel{self.__channel}.wmv'
        self.channel_path = os.path.join(Controller.application_path, channel)
        self.__status = not self.__status
        if self.__status:
            Controller.PWR_STATUS = 'ON'
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.channel_path)))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
        elif self.__status == False:
            Controller.PWR_STATUS = 'OFF'
            self.mediaPlayer.stop()
            self.label_info.setText('')
        self.label_power.setText(f'Power = {Controller.PWR_STATUS}')

    def volume_up(self) -> None:
        """
        Method to increase current volume of mediaPlayer content.
        Unmutes when method is called.
        """
        if self.__status:
            self.mediaPlayer.setMuted(False)
            self.__volume += 20
            self.mediaPlayer.setVolume(self.__volume)
            if self.__volume > Controller.MAX_VOLUME:
                self.__volume = Controller.MAX_VOLUME
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def volume_down(self) -> None:
        """
        Method to decrease current volume of mediaPlayer content.
        Unmutes when method is called.
        """
        if self.__status:
            self.mediaPlayer.setMuted(False)
            self.__volume -= 20
            self.mediaPlayer.setVolume(self.__volume)
            if self.__volume < Controller.MIN_VOLUME:
                self.__volume = Controller.MIN_VOLUME
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def mute(self) -> None:
        """
        Method that mutes or unmutes mediaPlayer content.
        Stays muted, until called upon again, even when turning TV on and off or changing channels.
        """
        if self.__status == True and self.mediaPlayer.isMuted() == False:
            self.mediaPlayer.setMuted(True)
            self.mediaPlayer.setVolume(0)
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
        elif self.__status == True and self.mediaPlayer.isMuted() == True:
            self.mediaPlayer.setMuted(False)
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def channel_up(self) -> None:
        """
        Method to decrease current channel number and display new channel.
        Loops current channel number to MIN_CHANNEL value when increased beyond MAX_CHANNEL value.
        """
        if self.__status:
            self.__channel += 1
            if self.__channel > Controller.MAX_CHANNEL:
                self.__channel = Controller.MIN_CHANNEL
            channel = f'channel{self.__channel}.wmv'
            self.channel_path = os.path.join(Controller.application_path, channel)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.channel_path)))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def channel_down(self) -> None:
        """
        Method to decrease current channel number and display new channel.
        Loops current channel number to MAX_CHANNEL value when decreased below MIN_CHANNEL value.
        """
        if self.__status:
            self.__channel -= 1
            if self.__channel < Controller.MIN_CHANNEL:
                self.__channel = Controller.MAX_CHANNEL
            channel = f'channel{self.__channel}.wmv'
            self.channel_path = os.path.join(Controller.application_path, channel)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.channel_path)))
            self.mediaPlayer.play()
            self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')

    def numpad_pressed(self, numpad_num: int) -> None:
        """
        Method to change channel in accordance with what numpad button is pressed, and
        warns user of unavailable channel when value of numpad button pressed excedes current MAX_CHANNEL value.
        :param numpad_num: Number associated with the specific numpad button pressed, int value.
        """
        if self.__status:
            if numpad_num in range(Controller.MIN_CHANNEL, Controller.MAX_CHANNEL + 1):
                if self.__channel != numpad_num:
                    self.__channel = numpad_num
                    channel = f'channel{self.__channel}.wmv'
                    self.channel_path = os.path.join(Controller.application_path, channel)
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.channel_path)))
                    self.mediaPlayer.play()
                    self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
                else:
                    self.label_info.setText(f'Channel = {self.__channel}  Volume = {self.mediaPlayer.volume()}')
            else:
                self.label_info.setText(f'Channel {numpad_num} not currently available')

    def channel_list(self) -> None:
        """
        Method to display currently available channel numbers ranging between MIN_CHANNEL and MAX_CHANNEL inclusively.
        """
        if self.__status:
            self.label_info.setText(f'Channels Available: {Controller.MIN_CHANNEL}-{Controller.MAX_CHANNEL}')
