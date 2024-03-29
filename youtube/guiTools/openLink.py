import pyperclip
import webbrowser
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
from settings import *
language.init_translation()
class openLink (qt.QDialog):
    def __init__(self,p,link):
        super().__init__(p)
        self.setWindowTitle(_("Open link dialog"))
        label=qt.QLabel(_("link"))
        self.link=qt.QLineEdit()
        self.link.setReadOnly(True)
        self.link.setText(link)
        self.link.setAccessibleName(_("link"))
        self.open=qt.QPushButton(_("open link "))
        self.open.clicked.connect(self.fopen)
        self.copy=qt.QPushButton(_("copy link"))
        self.copy.clicked.connect(self.fcopy)
        layout=qt.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.link)
        layout.addWidget(self.open)
        layout.addWidget(self.copy)
        self.setLayout(layout)
    def fopen(self):
        webbrowser.open(self.link.text())
        self.close()
    def fcopy(self):
        pyperclip.copy(self.link.text())
        self.close()
def OpenLink (p,Link):
	openLink (p,Link).exec()