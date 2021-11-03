# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, \
                                QMainWindow, \
                                QFileDialog

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from lindu.Widgets.Settings.LStyle import LStyle
from lindu.Widgets.LTomography.LT2D.tabCreateModel import mainModelDisplay

class LT2DCreateModel(QMainWindow):
    def __init__(self, parent = None):
        super(LT2DCreateModel, self).__init__(parent)
        self.load_ui()
        self.ui_settings()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent.parent.parent / "ui/LT2DCreateModel.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        self.setCentralWidget(self.ui)
        self.setGeometry(self.ui.geometry())
        center = QApplication.primaryScreen().availableGeometry().center()
        frameGeom = self.frameGeometry()
        frameGeom.moveCenter(center)
        self.move(frameGeom.topLeft())
        # self.setStyleSheet(LStyle())
        ui_file.close()

    def ui_settings(self):
        self.ui.model_tab.tabCloseRequested.connect(self.closeViewTab)
        self.ui.actionImport_Picture.triggered.connect(self.importPicture)
    
    def closeViewTab(self, currentIndex):
        currentQWidget = self.ui.model_tab.widget(currentIndex)
        currentQWidget.deleteLater()
        self.ui.model_tab.removeTab(currentIndex)

    def importPicture(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open picture file', '/',"Format File (*.jpg *.jpeg)")

        if filepath[0] != '':
            picCanvas = mainModelDisplay(filepath[0])
            dir, fil = os.path.split(filepath[0])
            self.ui.model_tab.addTab(picCanvas,fil)
