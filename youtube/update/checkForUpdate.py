import settings
from .updater import DownloadUpdateGUI
import requests
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from settings.app import appdirname
def check (p,message=True):
    try:
        r=requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/{}/update/app.json".format(settings.settings_handler.appName,appdirname))
        info=r.json()
        if info["version"]>settings.app.version:
            if info["is_beta"] and settings.settings_handler.get("update","beta")=="False":
                if message: qt.QMessageBox.information(p,_("info"),_("no updates fownd"))
            else:
                download(p,info["version"],info["download"],info["what is new"]).exec()
        else:
            if message: qt.QMessageBox.information(p,_("info"),_("no updates fownd"))
    except:
        if message: qt.QMessageBox.information(p,_("error"),_("server error please try later"))
class download (qt.QDialog):
    def __init__(self,p,version,URL,whatsNew):
        super().__init__(p)
        layout=qt.QVBoxLayout(self)
        self.setWindowTitle(_("new {} version {}").format(settings.app.name,str(version)))
        whatsn=qt.QLineEdit()
        whatsn.setReadOnly(True)
        whatsn.setAccessibleName(_("what's new"))
        whatsn.setText(whatsNew)
        self.URL=URL
        self.download=qt.QPushButton(_("download"))
        self.download.clicked.connect(lambda:DownloadUpdateGUI(self,URL).exec())
        self.Close=qt.QPushButton(_("close"))
        self.Close.clicked.connect(lambda:self.close())
        layout.addWidget(whatsn)
        layout.addWidget(self.download)
        layout.addWidget(self.Close)