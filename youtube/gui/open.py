import gui
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Open(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("open"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("link")))
        self.link=qt.QLineEdit()
        self.link.setAccessibleName(_("link"))
        layout.addWidget(self.link)
        layout.addWidget(qt.QLabel(_("type")))
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("type"))
        self.type.addItems([_("video"),_("playlist")])
        self.type.currentIndexChanged.connect(self.on_type)
        layout.addWidget(self.type)
        self.openVideo=qt.QPushButton(_("video actions"))
        self.openVideo.setDisabled(True)
        self.openVideo.clicked.connect(self.on_videoactions)
        layout.addWidget(self.openVideo)
        self.openPlaylist=qt.QPushButton(_("open playlist"))
        self.openPlaylist.setDisabled(True)
        self.openPlaylist.clicked.connect(lambda:gui.play.PlayPlayList(self,self.link.text()).exec())
        layout.addWidget(self.openPlaylist)
        self.on_type(self.type.currentIndex())
    def on_videoactions(self):
        PlayMenu=qt.QMenu()
        video=qt1.QAction(_("video"),self)
        PlayMenu.addAction(video)
        video.triggered.connect(lambda:gui.play.Play(self,self.link.text(),0).exec())
        audio=qt1.QAction(_("audio"),self)
        PlayMenu.addAction(audio)
        audio.triggered.connect(lambda:gui.play.Play(self,self.link.text(),1).exec())
        PlayMenu.exec()
    def on_type(self,index):
        self.openVideo.setDisabled(True)
        self.openPlaylist.setDisabled(True)
        if index==0:
            self.openVideo.setDisabled(False)
        elif index==1:
            self.openPlaylist.setDisabled(False)