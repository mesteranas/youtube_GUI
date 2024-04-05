from .comments import ViewComments
from . import channel
import guiTools,settings,gui
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
    def __init__(self,url,type):
        super().__init__()
        self.objects=PlayObjects()
        self.url=url
        self.type=type
    def run(self):
        guiTools.speak(_("loading"))
        self.video=YouTube(self.url)
        self.objects.finish.emit(self.video)
        if self.type==0:
            if settings.settings_handler.get("play","quality")=="0":
                self.objects.url.emit(self.video.streams.get_highest_resolution().url)
            else:
                self.objects.url.emit(self.video.streams.get_lowest_resolution().url)
        else:
            self.objects.url.emit(self.video.streams.filter(only_audio=True).first().url)
class Play(qt.QDialog):
    def __init__(self,p,videoURL,type):
        super().__init__(p)
        self.video=None
        thread=PlayThread(videoURL,type)
        thread.objects.finish.connect(self.on_finish_loading)
        thread.objects.url.connect(self.on_url)
        qt2.QThreadPool(self).start(thread)
        self.media=QMediaPlayer(self)
        self.position=0
        self.media.positionChanged.connect(self.on_position_changed)
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
        volume=player.addMenu(_("volume"))
        volume_up=qt1.QAction(_("volume up"),self)
        volume.addAction(volume_up)
        volume_up.setShortcut("alt+up")
        volume_up.triggered.connect(lambda:self.on_volume_control(self.audio.volume()+0.1))
        volume_down=qt1.QAction(_("volume down"),self)
        volume.addAction(volume_down)
        volume_down.setShortcut("alt+down")
        volume_down.triggered.connect(lambda:self.on_volume_control(self.audio.volume()-0.1))
        rate=player.addMenu(_("rate"))
        rate_plus=qt1.QAction(_("increase"),self)
        rate.addAction(rate_plus)
        rate_plus.setShortcut("f")
        rate_plus.triggered.connect(lambda:self.ofast("+"))
        rate_dash=qt1.QAction(_("decrease"),self)
        rate.addAction(rate_dash)
        rate_dash.setShortcut("shift+f")
        rate_dash.triggered.connect(lambda:self.ofast("-"))
        rate_normal=qt1.QAction(_("normal"),self)
        rate.addAction(rate_normal)
        rate_normal.setShortcut("ctrl+f")
        rate_normal.triggered.connect(lambda:self.ofast(1))
        video=menuBar.addMenu(_("video"))
        description=qt1.QAction(_("description"),self)
        video.addAction(description)
        description.triggered.connect(self.on_description)
        comments=qt1.QAction(_("comments"),self)
        video.addAction(comments)
        comments.triggered.connect(lambda:self.on_comments(videoURL))
        gotochannel=qt1.QAction(_("go to channel"),self)
        video.addAction(gotochannel)
        gotochannel.triggered.connect(self.on_go_to_channel)
        self.favorite=qt1.QAction(_("favorite"),self)
        video.addAction(self.favorite)
        self.favorite.setCheckable(True)
        self.favorite.triggered.connect(lambda:self.on_favorite(1))
        download=video.addMenu(_("download"))
        downloadVideo=qt1.QAction(_("video"),self)
        download.addAction(downloadVideo)
        downloadVideo.triggered.connect(self.on_download)
        downloadSubtitles=qt1.QAction(_("subtitles"),self)
        download.addAction(downloadSubtitles)
        downloadSubtitles.triggered.connect(self.on_download_subtitles)
        layout.setMenuBar(menuBar)
        qt1.QShortcut("escape",self).activated.connect(lambda:self.closeEvent(None))
    def on_play_pause(self):
        if self.media.isPlaying():
            self.media.pause()
        else:
            self.media.play()
    def closeEvent(self,event):
        gui.history.historyJsonControl.save(self.video.title + _("by") + self.video.author,self.position,self.video.watch_url)
        self.media.stop()
        self.close()
    def on_finish_loading(self,r):
        self.video=r
        self.setWindowTitle(self.video.title)
        self.favorite.setChecked(self.on_favorite(0))
    def on_url(self,url):
        self.url=url
        self.media.setSource(qt2.QUrl(self.url))
        self.media.play()
        guiTools.speak(_("loaded"))
        state,position,url=gui.history.historyJsonControl.get(self.video.title + _("by") + self.video.author)
        if state: self.media.setPosition(position)
    def on_description(self):
        self.media.pause()
        guiTools.TextViewer(self,_("description"),self.video.description).exec()
    def on_volume_control(self,volume):
        self.audio.setVolume(volume)
        guiTools.speak(str(self.audio.volume()*100).split(".")[0])
    def on_comments(self,url):
        self.media.pause()
        ViewComments(self,url).exec()
    def ofast(self,a):
        state=self.media.playbackRate()
        if state==0.1:
            pass
        elif state==2.0:
            pass
        else:
            if a=="-":
                self.media.setPlaybackRate(state - 0.1)
            elif a=="+":
                self.media.setPlaybackRate(state + 0.1)
            else:
                self.media.setPlaybackRate(1.0)
    def on_go_to_channel(self):
        self.media.pause()
        channel.OpenChannel(self,self.video.channel_id).exec()
    def on_favorite(self,index):
        text=self.video.title + _("by") + self.video.author
        data=gui.favorite.favoriteJsonControl.get("videos")
        if index==0:
            if data.get(text):
                return True
            else:
                return False
        else:
            if data.get(text):
                del(data[text])
            else:
                data[text]={"url":self.video.watch_url,"position":0}
            gui.favorite.favoriteJsonControl.save("videos",data)
    def on_position_changed(self,position):
        if position==0:
            return
        self.position=position
    def on_download(self):
        self.media.pause()
        gui.download.DownloadGUI(self,self.video.watch_url).exec()
    def on_download_subtitles(self):
        self.media.pause()
        gui.download.DownloadSubtitles(self,self.video.video_id).exec()