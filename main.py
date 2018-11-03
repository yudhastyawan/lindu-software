import sys
import time
import vtk
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from subroutine.icon.Icon import *

import module.Visualization.main as vis
import module.GAD.main as gad
import module.JHD.main as jhd
import module.hypoDD.main as hdd
import module.Tomography.main as tg

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.information_window()
        self.tab_main()

    def information_window(self):
        self.name_program = "Lindu ver 1.1"
        self.setWindowTitle(self.name_program)
        self.icon = QIcon(icon_window)
        self.setWindowIcon(self.icon)

    def tab_main(self):
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.tab_gs = QGroupBox()
        self.tab_vis = vis.MainWindow()
        self.tab_gad = gad.MainWindow()
        self.tab_jhd = jhd.MainWindow()
        self.tab_hdd = hdd.MainWindow()
        self.tab_tg = tg.MainWindow(self.tabs)

        # Tab Icon
        icon_tab_gs = QIcon()
        icon_tab_gs.addPixmap(QPixmap(icon_import), QIcon.Normal, QIcon.Off)
        icon_tab_vis = QIcon()
        icon_tab_vis.addPixmap(QPixmap(icon_datasets), QIcon.Normal, QIcon.Off)
        icon_tab_vis = QIcon()
        icon_tab_vis.addPixmap(QPixmap(icon_graph), QIcon.Normal, QIcon.Off)
        icon_tab_loc = QIcon()
        icon_tab_loc.addPixmap(QPixmap(icon_locate), QIcon.Normal, QIcon.Off)
        icon_tab_rel = QIcon()
        icon_tab_rel.addPixmap(QPixmap(icon_relocate), QIcon.Normal, QIcon.Off)
        icon_tab_tg = QIcon()
        icon_tab_tg.addPixmap(QPixmap(icon_tomo), QIcon.Normal, QIcon.Off)

        # Add tabs
        self.tabs.addTab(self.tab_gs, icon_tab_gs, "Getting Started")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_vis, icon_tab_vis, "Data Visualization")
        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_gad, icon_tab_loc, "Locate(GAD)")
        self.tabs.tabBar().setTabButton(2, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_jhd, icon_tab_rel, "Relocate(JHD)")
        self.tabs.tabBar().setTabButton(3, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_hdd, icon_tab_rel, "Relocate(DD)")
        self.tabs.tabBar().setTabButton(4, QTabBar.RightSide, None)
        self.tabs.addTab(self.tab_tg, icon_tab_tg, "Tomography")
        self.tabs.tabBar().setTabButton(5, QTabBar.RightSide, None)

        self.setCentralWidget(self.tabs)

    def closeTab (self, currentIndex):
        currentQWidget = self.tabs.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabs.removeTab(currentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    splash_pix = QPixmap(splash_screen)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(1)
    splash.close()
    main.showMaximized()
    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName(os.path.join(os.getcwd(),'bug','vtk.bug'))
    vtkStdErrOut = vtk.vtkOutputWindow()
    vtkStdErrOut.SetInstance(errOut)
    sys.exit(app.exec_())