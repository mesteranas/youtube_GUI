import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import requests
import guiTools,settings
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
        try:
            base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
            params = {
                "part": "snippet",
                "videoId": self.url,
                "key": settings.app.apiKey,
                "maxResults": 100,  # You can adjust this value based on your needs
            }
            all_comments = []
            next_page_token = None
            while True:
                if next_page_token:
                    params["pageToken"] = next_page_token
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    comments = data.get("items", [])
                    all_comments.extend(comments)
                    next_page_token = data.get("nextPageToken")
                    if not next_page_token:
                        break
                else:
                    self.comments={}
                    break
            if all_comments:
                for comment in all_comments:
                    snippet = comment["snippet"]["topLevelComment"]["snippet"]
                    author = snippet["authorDisplayName"]
                    text = snippet["textDisplay"]
                    self.comments[_("{} by {}").format(text,author)]=text
        except:
            self.comments={}
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