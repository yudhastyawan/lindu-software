# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import webbrowser

from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, Qt

from lindu.Widgets.Settings.LStyle import LStyle

class About(QDialog):
    def __init__(self, parent = None):
        super(About, self).__init__(parent)
        self.setWindowTitle("About Lindu")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(750, 573)
        self.load_ui()
        self.settings()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent.parent.parent / "ui/About.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.setGeometry(self.ui.geometry())
        center = QApplication.primaryScreen().availableGeometry().center()
        frameGeom = self.frameGeometry()
        frameGeom.moveCenter(center)
        self.move(frameGeom.topLeft())
        self.setStyleSheet(LStyle())
        ui_file.close()

    def settings(self):
        img_path = Path(__file__).resolve().parent.parent.parent
        self.ui.label_screen.setPixmap(QPixmap(os.path.join(img_path, "Images/larges/spl_scr.png")))
        self.ui.githubButton.clicked.connect(lambda: webbrowser.open("https://github.com/comp-geoph-itera/lindu-software/tree/package"))
        self.ui.docButton.clicked.connect(lambda: webbrowser.open("https://github.com/comp-geoph-itera/lindu-software/tree/package"))