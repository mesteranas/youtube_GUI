import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from youtubesearchpython import Comments
import guiTools
class CommentsObjects(qt2.QObject):
    finish=qt2.pyqtSignal(dict)
class CommentsThread(qt2.QRunnable):
    def __init__(self,url):
        super().__init__()
        self.objects=CommentsObjects()
        self.url=url
    def run(self):
        guiTools.speak(_("loading"))
        self.comments={}
        for comment in Comments(self.url).comments['result']:
            self.comments["{} by {}".format(comment['content'],comment['author']['name'])]=comment['content']
        self.objects.finish.emit(self.comments)

class ViewComments(qt.QDialog):
    def __init__(self,p,videoURL):
        super().__init__(p)
        self.setWindowTitle(_("comments"))
        self.comments={}
        thread=CommentsThread(videoURL)
        thread.objects.finish.connect(self.on_thread_finish)
        qt2.QThreadPool(self).start(thread)
        self.commentBox=qt.QListWidget()
        self.view=qt.QLineEdit()
        self.view.setReadOnly(True)
        self.view.setAccessibleName(_("comment text"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.commentBox)
        layout.addWidget(self.view)
        self.commentBox.currentTextChanged.connect(self.on_nav)
    def on_nav(self,text):
        self.view.setText(self.comments[text])
    def on_thread_finish(self,r):
        self.comments=r
        try:
            self.commentBox.addItems(self.comments)
            self.on_nav(list(self.comments.keys())[0])
        except:
            guiTools.speak(_("error"))
            self.close()
        self.commentBox.setFocus()
        guiTools.speak(_("loaded"))