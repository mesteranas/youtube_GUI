from youtubesearchpython import VideosSearch,PlaylistsSearch,ChannelsSearch
import gui
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class resultsObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict)
class resultsThread(qt2.QRunnable):
    def __init__(self,text,type):
        super().__init__()
        self.text=text
        self.type=type
        self.objects=resultsObjects()
    def run(self):
        guiTools.speak(_("searching"))
        videos={}
        if self.type==0:
            for video in VideosSearch(self.text).result()["result"]:
                videos["{} by {} {} ".format(video['title'],video['channel']['name'],video['viewCount']['short'])]=video['link']
        elif self.type==1:
            for video in PlaylistsSearch(self.text).result()["result"]:
                videos["{} by {}".format(video['title'],video['channel']['name'])]=f"https://www.youtube.com/playlist?list={video['id']}"
        elif self.type==2:
            for channel in ChannelsSearch(self.text).result()["result"]:
                videos[channel["title"]]=channel["id"]
        self.objects.finish.emit(videos)
class Results(qt.QDialog):
    def __init__(self,p,text,type):
        super().__init__(p)
        self.setWindowTitle(_("search results"))
        self.videos={}
        self.type=type
        thread=resultsThread(text,type)
        thread.objects.finish.connect(self.finishLoading)
        qt2.QThreadPool(self).start(thread)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("results")))
        self.results=qt.QListWidget()
        self.results.setAccessibleName(_("results"))
        self.results.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.results.customContextMenuRequested.connect(self.on_context)
        layout.addWidget(self.results)
        if self.type==0:
            self.play=qt.QPushButton(_("play"))
            self.play.clicked.connect(lambda:gui.play.Play(self,self.videos[self.results.currentItem().text()],0).exec())
            layout.addWidget(self.play)
        elif self.type==1:
            self.openPlaylist=qt.QPushButton(_("open playlist"))
            self.openPlaylist.clicked.connect(lambda:gui.play.PlayPlayList(self,self.videos[self.results.currentItem().text()]).exec())
            layout.addWidget(self.openPlaylist)
        elif self.type==2:
            self.openChannel=qt.QPushButton(_("open channel"))
            self.openChannel.clicked.connect(lambda:gui.play.OpenChannel(self,self.videos[self.results.currentItem().text()]).exec())
            layout.addWidget(self.openChannel)
    def finishLoading(self,r):
        self.videos=r
        self.results.addItems(self.videos.keys())
        self.results.setFocus()
        guiTools.speak(_("loaded"))
    def on_context(self):
        menu=qt.QMenu(self)
        if self.type==0:
            PlayMenu=menu.addMenu(_("play"))
            video=qt1.QAction(_("video"),self)
            PlayMenu.addAction(video)
            video.triggered.connect(lambda:gui.play.Play(self,self.videos[self.results.currentItem().text()],0).exec())
            audio=qt1.QAction(_("audio"),self)
            PlayMenu.addAction(audio)
            audio.triggered.connect(lambda:gui.play.Play(self,self.videos[self.results.currentItem().text()],1).exec())
        elif self.type==1:
            openplaylist=qt1.QAction(_("open playlist"),self)
            menu.addAction(openplaylist)
            openplaylist.triggered.connect(lambda:gui.play.PlayPlayList(self,self.videos[self.results.currentItem().text()]).exec())
        elif self.type==2:
            openChannel=qt1.QAction(_("open channel"),self)
            menu.addAction(openChannel)
            openChannel.triggered.connect(lambda:gui.play.OpenChannel(self,self.videos[self.results.currentItem().text()]).exec())
        openorcopyurl=qt1.QAction(_("open or copy url"),self)
        menu.addAction(openorcopyurl)
        openorcopyurl.triggered.connect(lambda:guiTools.OpenLink(self,self.videos[self.results.currentItem().text()]))
        menu.exec()