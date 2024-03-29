import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from pytube import YouTube
class Play(qt.QDialog):
    def __init__(self,p,videoURL):
        super().__init__(p)
        self.video=YouTube(videoURL)
        self.setWindowTitle(self.video.title)
        self.media=QMediaPlayer(self)
        layout=qt.QVBoxLayout(self)
        self.videoWidget=QVideoWidget()
        self.media.setVideoOutput(self.videoWidget)
        layout.addWidget(self.videoWidget)
        self.audio=QAudioOutput()
        self.media.setAudioOutput(self.audio)
        self.url=self.video.streams.get_lowest_resolution().url
        self.media.setSource(qt2.QUrl(self.url))
        self.media.play()