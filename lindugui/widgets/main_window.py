from pyface.qt import QtGui, QtCore
from lindugui.settings.styles import LStyle
from lindugui.settings.icon import icon, LIcon
from lindugui.widgets.menu_bar import LMenu

class LMainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(LMainWindow, self).__init__(parent)
        self.setStyleSheet(LStyle.MainWindow)
        self.threadpool = QtCore.QThreadPool()
        self.setWindowIcon(LIcon(icon.main_logo))

        self.mbar = self.menuBar()
        self.mFile = LMenu.addMenu('File',mbar=self.mbar,disabled=False)
        self.mQuit = LMenu.addAction('Quit',mbar=self.mFile,disabled=False,triggered=self.act_mQuit)

    def act_mQuit(self):
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    main = LMainWindow()
    main.show()
    app.exec_()