# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PySide2.QtGui import QIcon

from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from lindu.Widgets import LTomo2D, LTomo3D, LSeismoView, About, LStyle

version = "0.0.1"
develop = 1

class LinduWindow(QMainWindow):
    def __init__(self):
        super(LinduWindow, self).__init__()
        self.setWindowTitle("Lindu ver. " + version)
        self.setWindowIcon(QIcon(os.path.join(Path(__file__).resolve().parent, "Widgets/Images/icon/main_logo.png")))
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
        self.ui.lindu_tree.itemClicked.connect(lambda item, column: self.change_stack(item, column))
        self.ui.prog_check.stateChanged.connect(lambda: self.prog_check_changed(self.ui.prog_check))
    
    def stack_settings(self):
        tomo_2d = LTomo2D(self)
        self.ui.lindu_stack.insertWidget(0, tomo_2d)
        tomo_3d = LTomo3D(self)
        self.ui.lindu_stack.insertWidget(1, tomo_3d)
        seismo_view = LSeismoView(self)
        self.ui.lindu_stack.insertWidget(2, seismo_view)
        self.ui.lindu_stack.setCurrentIndex(1)

    def menu_settings(self):
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_about.triggered.connect(self.about_show)
    
    def prog_check_changed(self, check):
        if check.isChecked() == True:
            self.ui.lindu_tree.show()
        else:
            self.ui.lindu_tree.hide()
    
    def change_stack(self, item, column):
        current_text = item.text(column)
        if(current_text == "2D"):
            self.ui.lindu_stack.setCurrentIndex(0)
        elif(current_text == "3D"):
            self.ui.lindu_stack.setCurrentIndex(1)
        elif(current_text == "Seismo View"):
            self.ui.lindu_stack.setCurrentIndex(2)
    
    def about_show(self):
        about = About(self)
        about.show()
    
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                           quit_msg, QMessageBox.Yes, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def showEvent(self, event):
        if (develop == 1):
            msg = QMessageBox(self)
            msg.showEvent(event)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Lindu is still under development. However, you can still use some enabled features.")
            msg.setWindowTitle("Information")
            msg.show()    

def run():
    app = QApplication([])
    widget = LinduWindow()
    widget.show()
    app.exec_()
