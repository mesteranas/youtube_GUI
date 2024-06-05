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
        self.search=None
    def getNextResults(self):
        videos={}
        self.search.next()
        for video in self.search.result()["result"]:
            try:
                views=video['viewCount']['short']
            except:
                views=""
            try:
                auther=video['channel']['name']
            except:
                auther=""
            videos["{} by {} {} ".format(video['title'],auther,views)]=video['link']
        self.objects.finish.emit(videos)
    def run(self):
        guiTools.speak(_("searching"))
        videos={}
        if self.type==0:
            self.search=VideosSearch(self.text)
        elif self.type==1:
            self.search=PlaylistsSearch(self.text)
        elif self.type==2:
            self.search=ChannelsSearch(self.text)
        for video in self.search.result()["result"]:
            try:
                views=video['viewCount']['short']
            except:
                views=""
            try:
                auther=video['channel']['name']
            except:
                auther=""
            videos["{} by {} {} ".format(video['title'],auther,views)]=video['link']
        self.objects.finish.emit(videos)
class Results(qt.QDialog):
    def __init__(self,p,text,type):
        super().__init__(p)
        self.setWindowTitle(_("search results"))
        self.showFullScreen()
        self.videos={}
        self.type=type
        self.thread=resultsThread(text,type)
        self.thread.objects.finish.connect(self.finishLoading)
        qt2.QThreadPool(self).start(self.thread)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("results")))
        self.results=qt.QListWidget()
        self.results.setAccessibleName(_("results"))
        self.results.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.results.customContextMenuRequested.connect(self.on_context)
        self.results.currentRowChanged.connect(self.indexChanged)
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
            self.openChannel.clicked.connect(lambda:gui.play.OpenChannel(self,self.videos[self.results.currentItem().text()].split("/")[-1]).exec())
            layout.addWidget(self.openChannel)
    def finishLoading(self,r):
        index=self.results.currentIndex()
        # self.results.clear()
        self.videos=r
        self.results.addItems(self.videos.keys())
        self.results.setFocus()
        self.results.setCurrentIndex(index)
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
    def indexChanged(self,index):
        if index==self.results.count()-1:
            guiTools.speak(_("loading"))
            self.thread.getNextResults()