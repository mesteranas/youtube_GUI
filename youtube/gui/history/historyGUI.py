import gui
from . import historyJsonControl
import json
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class HistoryGUI(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("history"))
        self.videos={}
        for key,valu in json.load(open(historyJsonControl.path,"r",encoding="utf-8")).items():
            self.videos[key]=valu["url"]
        layout=qt.QVBoxLayout(self)
        self.history=qt.QListWidget()
        self.videosList=list(self.videos.keys())
        self.videosList.reverse()
        self.history.addItems(self.videosList)
        layout.addWidget(self.history)
        self.openVideo=qt.QPushButton(_("open video"))
        self.openVideo.clicked.connect(self.on_videoactions)
        layout.addWidget(self.openVideo)
    def on_videoactions(self):
        PlayMenu=qt.QMenu()
        video=qt1.QAction(_("video"),self)
        PlayMenu.addAction(video)
        video.triggered.connect(lambda:gui.play.Play(self,self.videos[self.history.currentItem().text()],0).exec())
        audio=qt1.QAction(_("audio"),self)
        PlayMenu.addAction(audio)
        audio.triggered.connect(lambda:gui.play.Play(self,self.videos[self.history.currentItem().text()],1).exec())
        PlayMenu.exec()
