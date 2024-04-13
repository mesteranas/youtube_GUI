import guiTools,gui
from pytube import Playlist
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class PlaylistObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict,Playlist)
class PlaylistThread(qt2.QRunnable):
    def __init__(self,playlistURL):
        super().__init__()
        self.objects=PlaylistObjects()
        self.playList=playlistURL
    def run(self):
        guiTools.speak(_("loading"))
        self.videos={}
        playlistSearch=Playlist(self.playList)
        for video in playlistSearch.videos:
            self.videos[video.title]=video.watch_url
        self.objects.finish.emit(self.videos,playlistSearch)
class PlayPlayList(qt.QDialog):
    def __init__(self,p,PlaylistUrl):
        super().__init__(p)
        self.showFullScreen()
        self.playlistDict={}
        self.videos={}
        thread=PlaylistThread(PlaylistUrl)
        thread.objects.finish.connect(self.on_finish_loading)
        qt2.QThreadPool(self).start(thread)
        layout=qt.QVBoxLayout(self)
        self.description=qt.QLineEdit()
        self.description.setReadOnly(True)
        layout.addWidget(self.description)
        self.playlistBox=qt.QListWidget()
        self.playlistBox.setAccessibleName(_("videos"))
        self.playlistBox.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlistBox.customContextMenuRequested.connect(self.on_context)
        layout.addWidget(self.playlistBox)
        self.play=qt.QPushButton(_("play"))
        self.play.clicked.connect(lambda:gui.play.Play(self,self.videos[self.playlistBox.currentItem().text()],0).exec())
        layout.addWidget(self.play)
        self.favorite=qt.QCheckBox(_("favorite"))

        layout.addWidget(self.favorite)
        self.goToChannel=qt.QPushButton(_("go to channel"))
        layout.addWidget(self.goToChannel)
    def on_finish_loading(self,r,pl):
        self.setWindowTitle(pl.title)
        self.description.setText(pl.description)
        self.playlistDict=pl
        self.favorite.setChecked(self.on_favorite(0))
        self.favorite.toggled.connect(lambda:self.on_favorite(1))
        self.goToChannel.clicked.connect(lambda:gui.play.OpenChannel(self,pl.owner_id).exec())
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
    def on_favorite(self,index):
        text=self.playlistDict.title + _("by") + self.playlistDict.owner
        data=gui.favorite.favoriteJsonControl.get("playlists")
        if index==0:
            if data.get(text):
                return True
            else:
                return False
        else:
            if data.get(text):
                del(data[text])
            else:
                data[text]={"url":"https://www.youtube.com/playlist?list="+self.playlistDict.playlist_id}
            gui.favorite.favoriteJsonControl.save("playlists",data)