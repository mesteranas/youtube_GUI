from .downloader import DownloaderGUI,DownloaderThread
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import pafy
class DownloadObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict)
class DownloadThread(qt2.QRunnable):
    def __init__(self,url):
        super().__init__()
        self.objects=DownloadObjects()
        self.url=url
    def run(self):
        guiTools.speak(_("loading"))
        downloadDict={}
        vid=pafy.new(self.url)
        for video in vid.streams:
            downloadDict["quality: {} type: {} extension : {}".format(video.resolution, _('video') if video.resolution else _('audio'),video.extension)]=[vid.title + "." + video.extension if video.extension else vid.title,video.url]
        self.objects.finish.emit(downloadDict)
class DownloadGUI(qt.QDialog):
    def __init__(self,p,url):
        super().__init__(p)
        self.setWindowTitle(_(" download video"))
        self.showFullScreen()
        self.videoQuality={}
        thread=DownloadThread(url)
        thread.objects.finish.connect(self.on_finish_loading)
        qt2.QThreadPool(self).start(thread)
        layout=qt.QVBoxLayout(self)
        self.path=qt.QLineEdit()
        self.path.setReadOnly(True)
        self.path.setAccessibleName(_("folder path"))
        layout.addWidget(self.path)
        self.select=qt.QPushButton(_("select folder"))
        self.select.clicked.connect(self.on_select)
        layout.addWidget(self.select)
        self.quality=qt.QListWidget()
        self.quality.setAccessibleName(_("select quality"))
        layout.addWidget(self.quality)
        self.download=qt.QPushButton(_("download"))
        self.download.clicked.connect(lambda:DownloaderGUI(self,self.videoQuality[self.quality.currentItem().text()],self.path.text()).exec())
        layout.addWidget(self.download)
    def on_select(self):
        folder=qt.QFileDialog(self)
        folder.setFileMode(qt.QFileDialog.FileMode.Directory)
        if folder.exec()==qt.QFileDialog.DialogCode.Accepted:
            self.path.setText(folder.selectedFiles()[0])
    def on_finish_loading(self,result):
        self.videoQuality=result
        self.quality.addItems(result)
        self.quality.setFocus()
        guiTools.speak(_("loaded"))