import guiTools,update
import zipfile
import sys
import os,shutil
from settings import settings_handler,app
from settings import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class PlaySettings(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        layout=qt.QFormLayout(self)
        self.quality=qt.QComboBox()
        self.quality.addItems([_("hi quality"),_("low quality")])
        self.quality.setCurrentIndex(int(settings_handler.get("play","quality")))
        layout.addRow(_("video quality"),self.quality)