import requests
import sys
import subprocess
import os,shutil
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class DownloadUpdateObjects(qt2.QObject):
    progress=qt2.pyqtSignal(int)
    installing=qt2.pyqtSignal(str)
    finish=qt2.pyqtSignal(str)
    download=qt2.pyqtSignal(bool)
class DownloadUpdateThread(qt2.QRunnable):
    def __init__ (self,URL):
        super().__init__()
        self.URL=URL
        self.object=DownloadUpdateObjects()
        self.path="data/update"
        self.downloading=True
        self.object.download.connect(self.is_download)
    def is_download(self,value):
        self.downloading=value
    def run(self):
        Name=os.path.join(self.path,self.URL.split("/")[-1])
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        os.makedirs(self.path)
        try:
            with requests.get(self.URL,stream=True)as r:
                if r.status_code!=200:
                    self.object.finish.emit("error")
                    return
                size=r.headers.get("content-length")
                try:
                    size=int(size)
                except TypeError:
                    self.object.finish.emit("error")
                    return
                recieved=0
                progress=0
                with open(Name,"wb") as file:
                    for pk in r.iter_content(1024):
                        if not self.downloading:
                            file.close()
                            return
                        file.write(pk)
                        recieved+=len(pk)
                        progress=int((recieved/size)*100)
                        self.object.progress.emit(progress)
                self.object.installing.emit("yes")
        except:
            self.object.finish.emit("error")
        try:
            subprocess.Popen('"{}" /silent'.format(Name),shell=True)
        except:
            self.object.finish.emit("error")
        sys.exit()
class DownloadUpdateGUI (qt.QDialog):

    def __init__(self,p,URL):
        super().__init__(p)
        self.setWindowTitle(_("updating"))
        layout=qt.QVBoxLayout(self)
        self.state=qt.QLabel(_("downloading update please wait"))
        layout.addWidget(self.state)
        self.downloading=qt.QProgressBar()
        self.downloading.setRange(0,100)
        self.downloading.setAccessibleName(_("download state"))
        self.downloading.setValue(0)
        layout.addWidget(self.downloading)
        self.cancel=qt.QPushButton(_("cancel"))
        layout.addWidget(self.cancel)
        self.thread=qt2.QThreadPool(self)
        self.run=DownloadUpdateThread(URL)
        self.run.object.progress.connect(self.change)
        self.run.object.installing.connect(self.Installation)
        self.run.object.finish.connect(self.finish)
        self.thread.start(self.run)
        self.cancel.clicked.connect(self.cancelBTN)
    def Installation(self,choice):
        if choice=="yes":
            self.state.setText(_("installing"))
            self.downloading.setValue(0)
    def change(self,progress):
        self.downloading.setValue(progress)
    def finish(self,c):
        if c=="error":
            qt.QMessageBox.information(self,"error","error while downloading")
            self.close()
    def cancelBTN(self):
        self.run.object.download.emit(False)
        self.close()