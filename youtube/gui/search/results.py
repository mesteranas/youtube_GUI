from pytube import Search
import gui
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class resultsObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict)
class resultsThread(qt2.QRunnable):
    def __init__(self,text):
        super().__init__()
        self.text=text
        self.objects=resultsObjects()
    def run(self):
        guiTools.speak(_("searching"))
        videos={}
        for video in Search(self.text).results:
            videos["{} by {} {} views".format(video.title, video.author, video.views)] = video.watch_url
        self.objects.finish.emit(videos)

class Results(qt.QDialog):
    def __init__(self,p,text):
        super().__init__(p)
        self.setWindowTitle(_("search results"))
        self.videos={}
        thread=resultsThread(text)
        thread.objects.finish.connect(self.finishLoading)
        qt2.QThreadPool(self).start(thread)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("results")))
        self.results=qt.QListWidget()
        self.results.setAccessibleName(_("results"))
        layout.addWidget(self.results)
        self.play=qt.QPushButton(_("play"))
        self.play.clicked.connect(lambda:gui.play.Play(self,self.videos[self.results.currentItem().text()]).exec())
        layout.addWidget(self.play)
    def finishLoading(self,r):
        self.videos=r
        self.results.addItems(self.videos.keys())
        self.results.setFocus()
        guiTools.speak(_("loaded"))