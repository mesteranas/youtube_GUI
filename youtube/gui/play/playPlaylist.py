import guiTools,gui
from pytube import Playlist
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class PlaylistObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict)
class PlaylistThread(qt2.QRunnable):
    def __init__(self,playlistURL):
        super().__init__()
        self.objects=PlaylistObjects()
        self.playList=playlistURL
    def run(self):
        guiTools.speak(_("loading"))
        self.videos={}
        for video in Playlist(self.playList).videos:
            self.videos[video.title]=video.watch_url
        self.objects.finish.emit(self.videos)
class PlayPlayList(qt.QDialog):
    def __init__(self,p,PlaylistUrl):
        super().__init__(p)
        self.videos={}
        self.setWindowTitle(_("playlist"))
        thread=PlaylistThread(PlaylistUrl)
        thread.objects.finish.connect(self.on_finish_loading)
        qt2.QThreadPool(self).start(thread)
        layout=qt.QVBoxLayout(self)
        self.playlistBox=qt.QListWidget()
        self.playlistBox.setAccessibleName(_("videos"))
        self.playlistBox.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlistBox.customContextMenuRequested.connect(self.on_context)
        layout.addWidget(self.playlistBox)
        self.play=qt.QPushButton(_("play"))
        self.play.clicked.connect(lambda:gui.play.Play(self,self.videos[self.playlistBox.currentItem().text()],0).exec())
        layout.addWidget(self.play)
    def on_finish_loading(self,r):
        self.videos=r
        self.playlistBox.addItems(self.videos.keys())
        self.playlistBox.setFocus()
        guiTools.speak(_("loaded"))
    def on_context(self):
        menu=qt.QMenu(self)
        PlayMenu=menu.addMenu(_("play"))
        video=qt1.QAction(_("video"),self)
        PlayMenu.addAction(video)
        video.triggered.connect(lambda:gui.play.Play(self,self.videos[self.playlistBox.currentItem().text()],0).exec())
        audio=qt1.QAction(_("audio"),self)
        PlayMenu.addAction(audio)
        audio.triggered.connect(lambda:gui.play.Play(self,self.videos[self.playlistBox.currentItem().text()],1).exec())
        openorcopyurl=qt1.QAction(_("open or copy url"),self)
        menu.addAction(openorcopyurl)
        openorcopyurl.triggered.connect(lambda:guiTools.OpenLink(self,self.videos[self.results.currentItem().text()]))
        menu.exec()