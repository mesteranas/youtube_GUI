from .results import Results
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Search(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("search"))
        self.showFullScreen()
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("search")))
        self.searchBox=qt.QLineEdit()
        self.searchBox.setAccessibleName(_("search"))
        layout.addWidget(self.searchBox)
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("type"))
        self.type.addItems([_("video"),_("play list"),_("channel")])
        layout.addWidget(self.type)
        self.searchButton=qt.QPushButton(_("search"))
        self.searchButton.clicked.connect(self.on_search)
        layout.addWidget(self.searchButton)
        self.cancel=qt.QPushButton(_("close"))
        self.cancel.clicked.connect(lambda:self.close())
        layout.addWidget(self.cancel)
    def on_search(self):
        Results(self,self.searchBox.text(),self.type.currentIndex()).exec()
        self.close()