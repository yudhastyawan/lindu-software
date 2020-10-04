import sys
import time
from pyface.qt import QtGui, QtCore

from subroutine.icon.Icon import *

# import module.Tomography.submodule.analyze2D.submodule.createvel2d as cv2d
import module.Tomography.submodule.analyze2D.submodule.fwdmodel as fwd
import module.Tomography.submodule.analyze2D.submodule.crtmodel as crt
import module.Tomography.submodule.analyze2D.submodule.invModel as invM

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.tab_main()

    def tab_main(self):
        # Initialize tab screen
        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        # self.tab_cv2d = cv2d.MainWindow()
        self.tab_fwd = fwd.MainWindow()
        self.tab_crt = crt.MainWindow()
        self.tab_inv = invM.MainWindow()

        # Tab Icon
        icon_tab_cv2d = QtGui.QIcon()
        icon_tab_cv2d.addPixmap(QtGui.QPixmap(icon_tomo), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # Add tabs
        # self.tabs.addTab(self.tab_cv2d, icon_tab_cv2d, "Create Model")
        # self.tabs.tabBar().setTabButton(0, QtGui.QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_fwd, icon_tab_cv2d, "Forward Modeling")
        self.tabs.tabBar().setTabButton(1, QtGui.QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_crt, icon_tab_cv2d, "CRT Modeling")
        self.tabs.tabBar().setTabButton(2, QtGui.QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_inv, icon_tab_cv2d, "Inverse Modeling")
        self.tabs.tabBar().setTabButton(3, QtGui.QTabBar.RightSide, None)

        self.setCentralWidget(self.tabs)

    def closeTab (self, currentIndex):
        currentQWidget = self.tabs.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabs.removeTab(currentIndex)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())