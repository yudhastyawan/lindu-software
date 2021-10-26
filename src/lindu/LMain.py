# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from lindu.Widgets import LTomo2D, LTomo3D, About, LStyle

version = "0.2.0"

class LinduWindow(QMainWindow):
    def __init__(self):
        super(LinduWindow, self).__init__()
        self.setWindowTitle("Lindu ver. " + version)
        self.load_ui()
        self.stack_settings()
        self.menu_settings()
        self.ui_settings()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "Widgets/ui/LMain.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        self.setCentralWidget(self.ui)
        self.setGeometry(self.ui.geometry())
        center = QApplication.primaryScreen().availableGeometry().center()
        frameGeom = self.frameGeometry()
        frameGeom.moveCenter(center)
        self.move(frameGeom.topLeft())
        self.setStyleSheet(LStyle())
        ui_file.close()
    
    def ui_settings(self):
        self.ui.lindu_tree.expandAll()
    
    def stack_settings(self):
        tomo_2d = LTomo2D(self)
        self.ui.lindu_stack.insertWidget(0, tomo_2d)
        tomo_3d = LTomo3D(self)
        self.ui.lindu_stack.insertWidget(1, tomo_3d)
        self.ui.lindu_stack.setCurrentIndex(1)

    def menu_settings(self):
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_about.triggered.connect(self.about_show)
        self.ui.lindu_tree.itemClicked.connect(lambda item, column: self.change_stack(item, column))
    
    def change_stack(self, item, column):
        current_text = item.text(column)
        if(current_text == "2D"):
            self.ui.lindu_stack.setCurrentIndex(0)
        elif(current_text == "3D"):
            self.ui.lindu_stack.setCurrentIndex(1)
    
    def about_show(self):
        about = About(self)
        about.show()

def run():
    app = QApplication([])
    widget = LinduWindow()
    widget.show()
    sys.exit(app.exec_())
