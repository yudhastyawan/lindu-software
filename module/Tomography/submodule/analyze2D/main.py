import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from subroutine.icon.Icon import *

import module.Tomography.submodule.analyze2D.submodule.createvel2d as cv2d
import module.Tomography.submodule.analyze2D.submodule.fwdmodel as fwd
import module.Tomography.submodule.analyze2D.submodule.crtmodel as crt
import module.Tomography.submodule.analyze2D.submodule.invModel as invM

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.tab_main()

    def tab_main(self):
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.tab_cv2d = cv2d.MainWindow()
        self.tab_fwd = fwd.MainWindow()
        self.tab_crt = crt.MainWindow()
        self.tab_inv = invM.MainWindow()

        # Tab Icon
        icon_tab_cv2d = QIcon()
        icon_tab_cv2d.addPixmap(QPixmap(icon_tomo), QIcon.Normal, QIcon.Off)

        # Add tabs
        self.tabs.addTab(self.tab_cv2d, icon_tab_cv2d, "Create Model")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_fwd, icon_tab_cv2d, "Forward Modeling")
        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_crt, icon_tab_cv2d, "CRT Modeling")
        self.tabs.tabBar().setTabButton(2, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_inv, icon_tab_cv2d, "Inverse Modeling")
        self.tabs.tabBar().setTabButton(3, QTabBar.RightSide, None)

        self.setCentralWidget(self.tabs)

    def closeTab (self, currentIndex):
        currentQWidget = self.tabs.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabs.removeTab(currentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())