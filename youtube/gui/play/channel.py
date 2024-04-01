import gui,guiTools
from youtubesearchpython import Channel,Playlist,playlist_from_channel_id
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class channelPlaylist(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        self.p=p
        layout=qt.QVBoxLayout(self)
        self.playlistBox=qt.QListWidget()
        layout.addWidget(self.playlistBox)
        self.openPlaylist=qt.QPushButton(_("open playlist"))
        self.openPlaylist.clicked.connect(lambda:gui.play.PlayPlayList(self,self.p.playlists[self.playlistBox.currentItem().text()]).exec())
        layout.addWidget(self.openPlaylist)

class ChannelVideos(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        self.p=p
        layout=qt.QVBoxLayout(self)
        self.videosBox=qt.QListWidget()
        self.videosBox.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.videosBox.customContextMenuRequested.connect(self.on_videoactions)

        layout.addWidget(self.videosBox)
        self.play=qt.QPushButton(_("play"))
        self.play.clicked.connect(lambda:gui.play.Play(self,self.p.videos[self.videosBox.currentItem().text()],0).exec())
        layout.addWidget(self.play)
    def on_videoactions(self):
        PlayMenu=qt.QMenu()
        video=qt1.QAction(_("play as video"),self)
        PlayMenu.addAction(video)
        video.triggered.connect(lambda:gui.play.Play(self,self.p.videos[self.videosBox.currentItem().text()],0).exec())
        audio=qt1.QAction(_("play as audio"),self)
        PlayMenu.addAction(audio)
        audio.triggered.connect(lambda:gui.play.Play(self,self.p.videos[self.videosBox.currentItem().text()],1).exec())
        PlayMenu.exec()

class ChannelInfo(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.description=qt.QLineEdit()
        self.description.setReadOnly(True)
        layout.addWidget(self.description)
        self.info=qt.QListWidget()
        layout.addWidget(self.info)
class ChannelObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict,int)
class channelThread(qt2.QRunnable):
    def __init__(self,channelURL):
        super().__init__()
        self.objects=ChannelObjects()
        self.channelURL=channelURL
    def run(self):
        guiTools.speak(_("loading"))
        self.objects.finish.emit(Channel.get(self.channelURL),0)
        self.videos={}
        plv=Playlist(playlist_from_channel_id(self.channelURL))
        while plv.hasMoreVideos:
            plv.getNextVideos()
        for video in plv.videos:
            self.videos[video["title"]]=video["link"]
        self.objects.finish.emit(self.videos,1)
        playlists={}
        channelplaylist=Channel(self.channelURL)
        """
        while channelplaylist.has_more_playlists:
            channelplaylist.next()
        """
        for pl in channelplaylist.result["playlists"]:
            playlists[pl["title"]]="https://www.youtube.com/playlist?list=" + pl["id"]
        self.objects.finish.emit(playlists,2)

class OpenChannel(qt.QDialog):
    def __init__(self,p,channelURL):
        super().__init__(p)
        thread=channelThread(channelURL)
        thread.objects.finish.connect(self.on_finish_loading)
        qt2.QThreadPool(self).start(thread)
        self.channel=None
        self.videos={}
        layout=qt.QVBoxLayout(self)
        self.tab=qt.QTabWidget()
        self.channelInfo=ChannelInfo(self)
        self.tab.addTab(self.channelInfo,_("information"))
        self.channelVideos=ChannelVideos(self)
        self.tab.addTab(self.channelVideos,_("videos"))
        self.playlist=channelPlaylist(self)
        self.tab.addTab(self.playlist,_("playlists"))
        self.playlists={}
        layout.addWidget(self.tab)
    def on_finish_loading(self,result,index):
        if index==0:
            self.channel=result
            self.setWindowTitle(self.channel["title"])
            self.channelInfo.description.setText(self.channel["description"])
            self.channelInfo.info.clear()
            self.channelInfo.info.addItems([_("subscribers {}".format(self.channel["subscribers"]["label"])),_("views  {}".format(self.channel["views"])),_("joined date {}".format(self.channel["joinedDate"])),_("country {}".format(self.channel["country"]))])
            guiTools.speak(_("information loaded"))
        elif index==1:
            self.videos=result
            self.channelVideos.videosBox.addItems(self.videos)
            guiTools.speak(_("videos loaded"))
        elif index==2:
            self.playlists=result
            self.playlist.playlistBox.addItems(self.playlists)
            guiTools.speak(_("playlists loaded"))