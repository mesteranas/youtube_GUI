import os,sys
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
from settings import *
language.init_translation()
class ExitApp (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("exit {} dialog").format(app.name))
        self.cancel1=False
        lec=_("what woud you like to do?")
        label=qt.QLabel(lec)
        self.exit=qt.QComboBox()
        self.exit.setAccessibleName(lec)
        self.exit.addItems([_("exit"),_("restart")])
        self.ok=qt.QPushButton(_("OK"))
        self.ok.clicked.connect(self.fok)
        self.cancel=qt.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.fcan)
        layout=qt.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.exit)
        layout.addWidget(self.ok)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        ec=self.exit.currentIndex()
        if ec==0:
            sys.exit()
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)
    def fcan(self):
        self.cancel1=True
        self.close()
