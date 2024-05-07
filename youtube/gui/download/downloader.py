import guiTools
import os
import requests
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class DownloaderObjects(qt2.QObject):
    progressBar=qt2.pyqtSignal(int)
    finish=qt2.pyqtSignal(bool)
class DownloaderThread(qt2.QRunnable):
    def __init__(self,fun,path):
        super().__init__()
        self.objects=DownloaderObjects()
        self.fun=fun
        self.path=path
    def run(self):
        with requests.get(self.fun[1],stream=True)as r:
            if r.status_code!=200:
                self.objects.finish.emit(False)
                return
            size=r.headers.get("content-length")
            try:
                size=int(size)
            except:
                self.objects.finish.emit(False)
                return
            recieved=0
            progress=0
            with open(os.path.join(self.path,self.fun[0]),"wb") as file:
                for bart in r.iter_content(1024):
                    file.write(bart)
                    recieved+=len(bart)
                    progress=int((recieved/size)*100)
                    self.objects.progressBar.emit(progress)
        self.objects.finish.emit(True)
class DownloaderGUI(qt.QDialog):
    def __init__(self,p,fun,path):
        super().__init__(p)
        thread=DownloaderThread(fun,path)
        thread.objects.progressBar.connect(self.on_progress)
        thread.objects.finish.connect(self.on_finish)
        qt2.QThreadPool(self).start(thread)
        self.setWindowTitle(_("downloading"))
        self.showFullScreen()
        self.progressBar=qt.QProgressBar()
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.progressBar)
        qt1.QShortcut("d",self).activated.connect(lambda:guiTools.speak(str(self.progressBar.value())))
    def on_progress(self,value):
        self.progressBar.setValue(value)
    def on_finish(self,state):
        if state:
            qt.QMessageBox.information(self,_("done"),_("downloaded"))
        else:
            qt.QMessageBox.warning(self,_("error"),_("please try later"))
        self.close()