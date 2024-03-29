import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from pytube import YouTube
class PlayObjects(qt2.QObject):
    finish=qt2.pyqtSignal(YouTube)
    url=qt2.pyqtSignal(str)
class PlayThread(qt2.QRunnable):
    def __init__(self,url):
        super().__init__()
        self.objects=PlayObjects()
        self.url=url
    def run(self):
        guiTools.speak(_("loading"))
        self.video=YouTube(self.url)
        self.objects.finish.emit(self.video)
        self.objects.url.emit(self.video.streams.get_lowest_resolution().url)
class Play(qt.QDialog):
    def __init__(self,p,videoURL):
        super().__init__(p)
        self.video=None
        thread=PlayThread(videoURL)
        thread.objects.finish.connect(self.on_finish_loading)
        thread.objects.url.connect(self.on_url)
        qt2.QThreadPool(self).start(thread)
        self.media=QMediaPlayer(self)
        layout=qt.QVBoxLayout(self)
        self.videoWidget=QVideoWidget()
        self.media.setVideoOutput(self.videoWidget)
        layout.addWidget(self.videoWidget)
        self.audio=QAudioOutput()
        self.media.setAudioOutput(self.audio)
        menuBar=qt.QMenuBar()
        player=menuBar.addMenu(_("player"))
        playPause=qt1.QAction(_("play / pause"),self)
        player.addAction(playPause)
        playPause.triggered.connect(self.on_play_pause)
        playPause.setShortcut("space")
        fastforward=qt1.QAction(_("fast forward"),self)
        player.addAction(fastforward)
        fastforward.triggered.connect(lambda:self.media.setPosition(self.media.position()+10000))
        fastforward.setShortcut("alt+right")
        rewind=qt1.QAction(_("rewind"),self)
        rewind.setShortcut("alt+left")
        player.addAction(rewind)
        rewind.triggered.connect(lambda:self.media.setPosition(self.media.position()-10000))
        volume_up=qt1.QAction(_("volume up"),self)
        player.addAction(volume_up)
        volume_up.setShortcut("alt+up")
        volume_up.triggered.connect(lambda:self.on_volume_control(self.audio.volume()+0.1))
        volume_down=qt1.QAction(_("volume down"),self)
        player.addAction(volume_down)
        volume_down.setShortcut("alt+down")
        volume_down.triggered.connect(lambda:self.on_volume_control(self.audio.volume()-0.1))
        video=menuBar.addMenu(_("video"))
        description=qt1.QAction(_("description"),self)
        video.addAction(description)
        description.triggered.connect(self.on_description)
        layout.setMenuBar(menuBar)
        qt1.QShortcut("escape",self).activated.connect(lambda:self.closeEvent(None))
    def on_play_pause(self):
        if self.media.isPlaying():
            self.media.pause()
        else:
            self.media.play()
    def closeEvent(self,event):
        self.media.stop()
        self.close()
    def on_finish_loading(self,r):
        self.video=r
        self.setWindowTitle(self.video.title)
    def on_url(self,url):
        self.url=url
        self.media.setSource(qt2.QUrl(self.url))
        self.media.play()
        guiTools.speak(_("loaded"))
    def on_description(self):
        self.media.pause()
        guiTools.TextViewer(self,_("description"),self.video.description).exec()
    def on_volume_control(self,volume):
        self.audio.setVolume(volume)
        guiTools.speak(str(self.audio.volume()*100).split(".")[0])