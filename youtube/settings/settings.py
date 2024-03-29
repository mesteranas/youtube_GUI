import guiTools,update
import zipfile
import sys
import os,shutil
from . import settings_handler,app,tabs
from . import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class settings (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("settings"))
        layout=qt.QVBoxLayout()
        self.sectian=guiTools.listBook(layout,_("select sectian"))
        self.update=tabs.Update(self)
        self.ok=qt.QPushButton(_("OK"))
        self.ok.clicked.connect(self.fok)
        self.defolt=qt.QPushButton(_("default"))
        self.defolt.clicked.connect(self.default)
        self.cancel=qt.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.fcancel)
        self.layout1=tabs.Genral(self)
        self.sectian.add(_("general"),self.layout1)
        self.sectian.add(_("update"),self.update)
        restoar=tabs.Restoar(self)
        self.sectian.add(_("Backup and restoar"),restoar)
        layout.addWidget(self.ok)
        layout.addWidget(self.defolt)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        aa=0
        if settings_handler.get("g","lang")!=str(language.lang()[self.layout1.language.currentText()]):
            aa=1
        settings_handler.set("g","lang",str(language.lang()[self.layout1.language.currentText()]))
        settings_handler.set("g","exitDialog",str(self.layout1.ExitDialog.isChecked()))
        settings_handler.set("update","autoCheck",str(self.update.update_autoDect.isChecked()))
        settings_handler.set("update","beta",str(self.update.update_beta.isChecked()))
        if aa==1:
            mb=qt.QMessageBox(self)
            mb.setWindowTitle(_("settings updated"))
            mb.setText(_("you must restart the program to apply changes \n do you want to restart now?"))
            rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
            rn.setText(_("restart now"))
            rl=mb.addButton(qt.QMessageBox.StandardButton.No)
            rl.setText(_("restart later"))
            mb.exec()
            ex=mb.clickedButton()
            if ex==rn:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif ex==rl:
                self.close()
        else:
            self.close()
    def default(self):
        mb=qt.QMessageBox(self)
        mb.setWindowTitle(_("alert"))
        mb.setText(_("do you wanna reset your settings ? \n if you click reset , the program will restart to complete reset."))
        rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
        rn.setText(_("reset and restart"))
        rl=mb.addButton(qt.QMessageBox.StandardButton.No)
        rl.setText(_("cancel"))
        mb.exec()
        ex=mb.clickedButton()
        if ex==rn:
            shutil.rmtree(os.path.join(os.getenv('appdata'),app.appName))
            os.execl(sys.executable, sys.executable, *sys.argv)

    def fcancel(self):
        self.close()
    def cbts(self,string):
        if string=="True":
            return True
        else:
            return False

