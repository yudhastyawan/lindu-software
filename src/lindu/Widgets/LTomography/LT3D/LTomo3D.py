# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from lindu.Widgets.Settings.LStyle import LStyle

class LTomo3D(QMainWindow):
    def __init__(self, parent = None):
        super(LTomo3D, self).__init__(parent)
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent.parent.parent / "ui/LTomo3D.ui")
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

