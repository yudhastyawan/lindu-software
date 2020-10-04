import sys
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
from pyface.qt import QtGui, QtCore
import time
import vtk

from subroutine.icon.Icon import *
from subroutine.plugins import plugins
# import module.Visualization.main as vis
# import module.GAD.main as gad
# import module.JHD.main as jhd
# import module.hypoDD.main as hdd
import module.Tomography.main as tg
from display import MayaviQWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.threadpool = QtCore.QThreadPool()
        self.information_window()
        self.menubar()

    def information_window(self):
        self.name_program = "Lindu Software ver. 0.1.0"
        self.setWindowTitle(self.name_program)
        self.icon = QtGui.QIcon(icon_window)
        self.setWindowIcon(self.icon)

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.mFile = self.mbar.addMenu('File')
        self.mOpen = self.mFile.addAction('Open')
        self.mProgram = self.mbar.addMenu('Programs')
        self.mHypo = self.mProgram.addMenu('Hypocenter')
        self.mLoc = self.mHypo.addAction('Location')
        self.mReloc = self.mHypo.addAction('Relocation')
        self.mTomo = self.mProgram.addAction('Traveltime Tomography')
        self.mPlug = plugins.Plugins(self.threadpool,self)
        self.mbar.addAction(self.mPlug.menuAction())
        self.mPlug.setTitle('Plugins')
        self.mHelp = self.mbar.addMenu('Help')
        self.mAbout = self.mHelp.addAction('About')
        self.mDoc = self.mHelp.addAction('Documentation')

        # add signal and slot to menubar
        self.mTomo.triggered.connect(self.act_mTomo)
        self.mOpen.triggered.connect(self.act_mOpen)


    def act_mTomo(self):
        tomoDialog = tg.MainWindow(self)
        frameGm = tomoDialog.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        tomoDialog.move(frameGm.topLeft())
        tomoDialog.show()

    def act_mOpen(self):
        logdata = os.path.join(os.getcwd(), 'tests', 'display', "15real.log")
        vdata = os.path.join(os.getcwd(), 'tests', 'display', "15vest.vel3d")
        xdata = os.path.join(os.getcwd(), 'tests', 'display', "15x.data")
        ydata = os.path.join(os.getcwd(), 'tests', 'display', "15y.data")
        zdata = os.path.join(os.getcwd(), 'tests', 'display', "15z.data")
        self.mayavi_widget = MayaviQWidget(logdata, vdata, xdata, ydata, zdata)
        frameGm = self.mayavi_widget.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        self.mayavi_widget.move(frameGm.topLeft())
        self.mayavi_widget.show()

    def closeEvent(self, event):
        if hasattr(self, 'mayavi_widget'):
            self.mayavi_widget.ui.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    splash_pix = QtGui.QPixmap(splash_screen)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(1)
    splash.close()
    main.show()
    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName(os.path.join(os.getcwd(), 'bug', 'vtk.bug'))
    vtkStdErrOut = vtk.vtkOutputWindow()
    vtkStdErrOut.SetInstance(errOut)
    sys.exit(app.exec_())