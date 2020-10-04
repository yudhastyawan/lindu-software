import sys
from pyface.qt import QtGui, QtCore
import os

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        newAction = QtGui.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)

        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)

        openAction = QtGui.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)

        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Window')
        closeAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)

        self.text = QtGui.QTextEdit(self)

        self.setCentralWidget(self.text)
        self.setGeometry(30, 30, 800, 500)
        self.setWindowTitle('Text Editor')
        self.icon = QtGui.QIcon(os.path.join(os.getcwd(),'subroutine','icon','Icon_Files','FIX','LOGO.ico'))
        self.setWindowIcon(self.icon)
        self.show()

    def newFile(self):
        self.text.clear()

    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
        f = open(filename, 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        f = open(filename, 'r')
        filedata = f.read()
        self.text.setText(filedata)
        f.close()


def main():
    app = QtGui.QApplication(sys.argv)
    notepad = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
