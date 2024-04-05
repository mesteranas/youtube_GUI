from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class DownloadSubtitles(qt.QDialog):
    def __init__(self,p,VideoId):
        super().__init__(p)
        layout=qt.QVBoxLayout(self)
        self.path=qt.QLineEdit()
        self.path.setAccessibleName(_("path"))
        self.path.setReadOnly(True)
        layout.addWidget(self.path)
        self.select=qt.QPushButton(_("select"))
        self.select.clicked.connect(self.on_select)
        layout.addWidget(self.select)
        layout.addWidget(qt.QLabel(_("save as")))
        self.saveAS=qt.QComboBox()
        self.saveAS.addItems([_("text"),"html","srt"])
        self.saveAS.setAccessibleName(_("save as"))
        layout.addWidget(self.saveAS)
        self.get=qt.QPushButton(_("get"))
        self.get.setDefault(True)
        self.get.clicked.connect(self.on_get)
        layout.addWidget(self.get)
        self.videoId=VideoId
    def on_get(self):
        try:
            html=[]
            text=[]
            srt=[]
            trans_list=YouTubeTranscriptApi.get_transcript(self.videoId)
            if trans_list:
                for i, transcript in enumerate(trans_list, start=1):
                    start_time = datetime.timedelta(seconds=transcript['start'])
                    end_time = datetime.timedelta(seconds=transcript['start'] + transcript['duration'])
                    srt.append(f"{i}\n{start_time} --> {end_time}\n{transcript['text']}\n")
                    text.append(transcript['text'])
                    html.append(f"<p>{transcript['text']}</p>")
            index=self.saveAS.currentIndex()
            with open(self.path.text(),"w",encoding="utf-8") as result:
                if index==0:
                    result.write("\n".join(text))
                elif index==1:
                    result.write("\n".join(html))
                else:
                    result.write("\n".join(srt))
                qt.QMessageBox.information(self,_("done"),_("downloaded"))
        except Exception as e:
            
            qt.QMessageBox.warning(self,_("error"),_("please try later"))
    def on_select(self):
        file=qt.QFileDialog(self)
        index=self.saveAS.currentIndex()
        if index==0:
            format="txt"
        elif index==1:
            format="html"
        else:
            format="srt"
        file.setDefaultSuffix(format)
        file.setAcceptMode(file.AcceptMode.AcceptSave)
        if file.exec()==file.DialogCode.Accepted:
            self.path.setText(file.selectedFiles()[0])