import sys
import os
import numpy as np
import matplotlib.image as mpimg

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mpl_toolkits.basemap import Basemap
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from subroutine.thread.threading import Worker, MessageBox, MessageOpt
from subroutine.time.tictac import tic, tac
from modules.Tomography.submodule.analyze2D.submodule.submodule.tabCreateModel import mainModelDisplay

class CreatePicNum(FigureCanvas):
    def __init__(self,pic,parent = None):

        img = mpimg.imread(pic)
        img2 = np.zeros((img.shape[0], img.shape[1]))
        for i in range(len(img[:,0,0])):
            for j in range(len(img[0,:,0])):
                img2[i,j] = img[i,j,:].mean()

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        pic = self.axes.imshow(img2, cmap='jet')
        self.fig.colorbar(pic)

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class OpenPicNum(QWidget):
    def __init__(self, path, parent = None):
        super(OpenPicNum, self).__init__(parent)
        self.mainLay = QHBoxLayout()
        self.setGroup = QGroupBox()
        self.viewPic = CreatePicNum(path)
        self.mainLay.addWidget(self.setGroup)
        self.mainLay.addWidget(self.viewPic)
        self.setLayout(self.mainLay)

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.menu_bar()
        self.main_widget()

    def main_widget(self):
        self.mainWid = QWidget()
        self.mainlay = QHBoxLayout()
        self.mainWid.setLayout(self.mainlay)
        self.setCentralWidget(self.mainWid)
        self.main_view_tab = QTabWidget()
        self.main_view_tab.setTabsClosable(True)
        self.main_view_tab.tabCloseRequested.connect(self.closeViewTab)
        self.mainlay.addWidget(self.main_view_tab)

    def menu_bar(self):
        self.mbar = self.menuBar()
        self.file = self.mbar.addMenu('File')
        self.imfig = self.file.addAction('Import Figure')

        # action
        self.imfig.triggered.connect(self.act_imfig)

    def act_imfig(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open picture file', '/',"Format File (*.jpg *.jpeg)")

        if filepath[0] != '':
            picCanvas = mainModelDisplay(filepath[0])
            dir, fil = os.path.split(filepath[0])
            self.main_view_tab.addTab(picCanvas,fil)

    def closeViewTab(self, currentIndex):
        currentQWidget = self.main_view_tab.widget(currentIndex)
        currentQWidget.deleteLater()
        self.main_view_tab.removeTab(currentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())
