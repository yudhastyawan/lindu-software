import sys
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
from pyface.qt import QtGui, QtCore
import time
import vtk
from copy import deepcopy as copy

from subroutine.icon.Icon import *
from subroutine.plugins import plugins
import module.Tomography.main as tg
import module.GAD.main as gad
import module.hypoDD.main as DD
import module.Visualization.main as Vis
from module.Displays import CubedView, Map

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.threadpool = QtCore.QThreadPool()
        self.information_window()
        self.menubar()
        self.mainWidget()
        self.setCentralWidget(self.mainWin)

    def information_window(self):
        self.name_program = "Lindu Software ver. 0.1.0"
        self.setWindowTitle(self.name_program)
        self.icon = QtGui.QIcon(icon_window)
        self.setWindowIcon(self.icon)

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.mFile = self.mbar.addMenu('File')
        self.mQuit = self.mFile.addAction('Quit')
        self.mProgram = self.mbar.addMenu('Programs')
        self.mVis = self.mProgram.addAction('Seismic View (BETA)')
        self.mHypo = self.mProgram.addMenu('Hypocenter')
        self.mLoc = self.mHypo.addAction('Location (GAD Wrapper)')
        self.mReloc = self.mHypo.addMenu('Relocation')
        self.mRelocDD = self.mReloc.addAction('HypoDD Wrapper')
        self.mRelocJHD = self.mReloc.addAction('JHD Wrapper')
        self.mTomo = self.mProgram.addAction('Traveltime Tomography')
        self.mProject = self.mbar.addMenu('Project')
        self.mProjectEarthTomo = self.mProject.addAction('Earthquake Tomography Project')
        self.mPlug = plugins.Plugins(self.threadpool,self)
        self.mbar.addAction(self.mPlug.menuAction())
        self.mPlug.setTitle('Plugins')
        self.mHelp = self.mbar.addMenu('Help')
        self.mAbout = self.mHelp.addAction('About')
        self.mDoc = self.mHelp.addAction('Documentation')
        self.mHelp.addSeparator()
        self.mDev = self.mHelp.addAction('Login as The Developer')

        # add signal and slot to menubar
        self.mTomo.triggered.connect(self.act_mTomo)
        self.mLoc.triggered.connect(self.act_mLoc)
        self.mRelocDD.triggered.connect(self.act_mRelocDD)
        self.mVis.triggered.connect(self.act_mVis)
        self.mQuit.triggered.connect(self.act_mQuit)

        # Disable premature function
        self.mProject.setDisabled(True)
        self.mHelp.setDisabled(True)
        self.mAbout.setDisabled(True)
        self.mDoc.setDisabled(True)
        self.mDev.setDisabled(True)
        self.mRelocJHD.setDisabled(True)

    def act_mQuit(self):
        self.close()

    def act_mVis(self):
        tomoDialog = Vis.MainWindow(self)
        frameGm = tomoDialog.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        tomoDialog.move(frameGm.topLeft())
        tomoDialog.showMaximized()

    def act_mRelocDD(self):
        tomoDialog = DD.MainWindow(self)
        frameGm = tomoDialog.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        tomoDialog.move(frameGm.topLeft())
        tomoDialog.show()

    def act_mLoc(self):
        tomoDialog = gad.MainWindow(self)
        frameGm = tomoDialog.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        tomoDialog.move(frameGm.topLeft())
        tomoDialog.show()

    def act_mTomo(self):
        tomoDialog = tg.MainWindow(self)
        frameGm = tomoDialog.frameGeometry()
        topLeftPoint = QtGui.QApplication.desktop().availableGeometry().topLeft()
        frameGm.moveTopLeft(topLeftPoint)
        tomoDialog.move(frameGm.topLeft())
        tomoDialog.show()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if hasattr(self, 'mayavi_widget'):
                self.mayavi_widget.ui.close()
            event.accept()
        else:
            event.ignore()

    def mainWidget(self):
        self.mainWin = QtGui.QWidget()
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainWin.setLayout(self.mainLayout)

        # main group
        self.setViewGroup = QtGui.QGroupBox()
        self.setViewGroup.setTitle("Settings")
        self.mainLayout.addWidget(self.setViewGroup,1)
        self.mainViewGroup = QtGui.QGroupBox()
        self.mainViewGroup.setTitle("Views")
        self.mainLayout.addWidget(self.mainViewGroup,3)

        # set View Group
        setViewLayout = QtGui.QVBoxLayout()
        self.setViewGroup.setLayout(setViewLayout)

        self.tabSetView = QtGui.QTabWidget()
        setViewLayout.addWidget(self.tabSetView)

        # main View Group
        mainViewLayout = QtGui.QVBoxLayout()
        self.mainViewGroup.setLayout(mainViewLayout)

        self.tabMainView = QtGui.QTabWidget()
        mainViewLayout.addWidget(self.tabMainView)
        self.tabMainView.setTabsClosable(True)
        self.tabMainView.tabCloseRequested.connect(self.closeTab)

        # filling set View Tab
        self.fillSetView()

    def fillSetView(self):
        # 3D Cubed Model
        self.Set3DCubedView = CubedView.SetView(self.tabMainView)
        self.tabSetView.addTab(self.Set3DCubedView,"3D Cube")
        self.SetMapView = Map.SetView(self.tabMainView)
        self.tabSetView.addTab(self.SetMapView, "Map")

    def closeTab (self, currentIndex):
        currentQWidget = self.tabMainView.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabMainView.removeTab(currentIndex)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    splash_pix = QtGui.QPixmap(splash_screen)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(1)
    splash.close()
    main.showMaximized()
    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName(os.path.join(os.getcwd(), 'bug', 'vtk.bug'))
    vtkStdErrOut = vtk.vtkOutputWindow()
    vtkStdErrOut.SetInstance(errOut)
    sys.exit(app.exec_())