import gui,guiTools
from . import favoriteJsonControl
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class FavoritGUI(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("favorites"))
        self.showFullScreen()
        self.dictionary={}
        layout=qt.QVBoxLayout(self)
        self.type=qt.QComboBox()
        self.type.addItems([_("videos"),_("playlists"),_("channels")])
        layout.addWidget(self.type)
        self.favorite=qt.QListWidget()
        layout.addWidget(self.favorite)
        self.go=qt.QPushButton(_("open"))
        self.go.clicked.connect(self.on_go)
        layout.addWidget(self.go)
        self.delete=qt.QPushButton(_("delete"))
        self.delete.setShortcut("delete")
        self.delete.clicked.connect(self.on_delete)
        layout.addWidget(self.delete)
        self.type.currentIndexChanged.connect(self.on_change)
        self.on_change(0)
    def on_change(self,index):
        self.favorite.clear()
        result=None
        if index==0:
            result=favoriteJsonControl.get("videos")
        elif index==1:
            result=favoriteJsonControl.get("playlists")
        elif index==2:
            result=favoriteJsonControl.get("channels")
        self.favorite.addItems(result)
        self.dictionary=result
    def on_videoactions(self):
        PlayMenu=qt.QMenu()
        video=qt1.QAction(_("video"),self)
        PlayMenu.addAction(video)
        video.triggered.connect(lambda:gui.play.Play(self,self.dictionary[self.favorite.currentItem().text()]["url"],0).exec())
        audio=qt1.QAction(_("audio"),self)
        PlayMenu.addAction(audio)
        audio.triggered.connect(lambda:gui.play.Play(self,self.dictionary[self.favorite.currentItem().text()]["url"],1).exec())
        PlayMenu.exec()
    def on_delete(self):
        text=""
        if self.type.currentIndex()==0:
            text="videos"
        elif self.type.currentIndex()==1:
            text="playlists"
        else:
            text="channels"
        try:
            data=favoriteJsonControl.get(text)
            del(data[self.favorite.currentItem().text()])
            favoriteJsonControl.save(text,data)
            self.on_change(self.type.currentIndex())
            guiTools.speak(_("deleted"))
        except:
            guiTools.speak(_("error"))
    def on_go(self):
        index=self.type.currentIndex()
        if index==0:
            self.on_videoactions()
        elif index==1:
            gui.play.PlayPlayList(self,self.dictionary[self.favorite.currentItem().text()]["url"]).exec()
        else:
            gui.play.OpenChannel(self,self.dictionary[self.favorite.currentItem().text()]["url"]).exec()