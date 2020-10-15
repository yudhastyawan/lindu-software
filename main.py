from lindugui import *

from lindugui.settings.icon import *
from lindugui.settings import plugins
import modules.Tomography.main as tg
import modules.GAD.main as gad
import modules.hypoDD.main as DD
from modules.Displays import CubedView, Map

class MainWindow(LMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.menubar()
        self.mainWidget()
        self.setCentralWidget(self.mainWin)
        self.setWindowTitle("Lindu Software")

    # create menubar
    def menubar(self):
        self.mProgram = LMenu.addMenu('Program',self.mbar)
        self.mHypo = LMenu.addMenu('Hypocenter',self.mProgram)
        self.mLoc = LMenu.addAction('Location (GAD Wrapper)',self.mHypo,triggered=self.act_mLoc)
        self.mReloc = LMenu.addMenu('Relocation',self.mHypo)
        self.mRelocDD = LMenu.addAction('HypoDD Wrapper',self.mReloc,triggered=self.act_mRelocDD)
        self.mRelocJHD = LMenu.addAction('JHD Wrapper',self.mReloc,disabled=True)
        self.mTomo = LMenu.addAction('Traveltime Tomography (BETA)',self.mProgram,triggered=self.act_mTomo)
        self.mProject = LMenu.addMenu('Project',self.mbar,disabled=True)
        self.mProjectEarthTomo = LMenu.addAction('Earthquake Tomography Project',self.mProject)
        # ====================
        self.mPlug = plugins.Plugins(self.threadpool,self)
        self.mbar.addAction(self.mPlug.menuAction())
        self.mPlug.setTitle('Plugins')
        # ====================
        self.mHelp = LMenu.addMenu('Help',self.mbar)
        self.mAbout = LMenu.addAction('About',self.mHelp,disabled=True)
        self.mDoc = LMenu.addAction('Documentation',self.mHelp,disabled=True)
        self.mHelp.addSeparator()
        self.mDev = LMenu.addAction('Login as The Developer',self.mHelp,disabled=True)

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
    splash_pix = QtGui.QPixmap(icon.splash_screen)
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