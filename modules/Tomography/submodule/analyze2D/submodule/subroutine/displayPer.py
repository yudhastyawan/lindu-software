import sys
import shutil
import numpy as np
import os
import sip

from pyface.qt.QtGui import *
from pyface.qt.QtCore import *
from tempfile import mkdtemp

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar

class rayDisplay(FigureCanvas):
    def __init__(self,vel,x,y,vmin,vmax,cmap,parent=None):

        self.fig = Figure()
        # self.ax1 = self.fig.add_subplot(121)
        # self.ax1.set_title('Ray Grid Resolution')
        # map = self.ax1.imshow(rgrid, cmap=cmap, extent=[x.min(), x.max(), y.max(), y.min()])
        # clb = self.fig.colorbar(map, orientation='horizontal')
        # clb.ax.set_title('N Ray')

        self.ax2 = self.fig.add_subplot(111)
        self.ax2.set_title('2D Velocity')
        map = self.ax2.imshow(vel, vmin=vmin, vmax=vmax, cmap=cmap, extent=[x.min(), x.max(), y.max(), y.min()])
        # for i in range(len(rpath[:, 0, 0])):
        #     self.ax2.plot(rpath[i, 0, :], rpath[i, 1, :], alpha=0.3)
        clb = self.fig.colorbar(map, orientation='horizontal')
        clb.ax.set_title('Pert vel (%)')
        self.fig.tight_layout()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class mainRayDisplay(QWidget):
    def __init__(self, velfile, parent = None):
        super(mainRayDisplay, self).__init__(parent)
        # filetemp = os.path.join(mkdtemp(), 'file.npz')
        # shutil.copyfile(rayfile, filetemp)
        # ray2d = np.load(filetemp)
        # rgrid = ray2d['grid']
        # rpath = ray2d['path']
        # self.rgrid = rgrid
        # self.rpath = rpath
        filetemp = os.path.join(mkdtemp(), 'file.npz')
        shutil.copyfile(velfile, filetemp)
        vel2d = np.load(filetemp)
        vel = vel2d['per']
        self.vel = vel
        x = vel2d['x']
        y = vel2d['y']
        self.x = x
        self.y = y

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        view_button = QPushButton()
        view_button.setText('View Scene')
        view_button.clicked.connect(self.view_click)
        view_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        laybutton = QHBoxLayout()
        laybutton.addWidget(view_button)

        # adding combo box
        self.colormap = QComboBox()
        self.colormap.addItem('jet')
        self.colormap.addItem('bwr')
        item = ['Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 'Greys', 'OrRd',
                'Oranges', 'PRGn', 'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu', 'PuBuGn', 'PuOr', 'PuRd', 'Purples',
                'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3', 'Spectral', 'Vega10',
                'Vega20', 'Vega20b', 'Vega20c', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn',
                'binary', 'black-white', 'blue-red', 'bone', 'brg', 'cool', 'coolwarm', 'copper', 'cubehelix', 'file',
                'flag', 'gist_earth', 'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 'gist_stern', 'gist_yarg',
                'gnuplot', 'gnuplot2', 'gray', 'hot', 'hsv', 'inferno', 'magma', 'nipy_spectral', 'ocean', 'pink',
                'plasma', 'prism', 'rainbow', 'seismic', 'spectral', 'spring', 'summer', 'terrain', 'viridis', 'winter']
        for i in range(len(item)):
            self.colormap.addItem(item[i])

        lb_colormap = QLabel()
        lb_colormap.setText('Colormap List')
        lb_colormap.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # adding vmin and vmax
        self.vmin = QLineEdit()
        self.vmin.setText(str(np.min(self.vel)))
        lb_vmin = QLabel()
        lb_vmin.setText('Color Min')
        lb_vmin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.vmax = QLineEdit()
        self.vmax.setText(str(np.max(self.vel)))
        lb_vmax = QLabel()
        lb_vmax.setText('Color Max')
        lb_vmax.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.check_reverse = QCheckBox()
        self.check_reverse.setText('reverse colormap')

        laybutton.addStretch()
        laybutton.addWidget(lb_vmin)
        laybutton.addWidget(self.vmin)
        laybutton.addWidget(lb_vmax)
        laybutton.addWidget(self.vmax)
        laybutton.addWidget(lb_colormap)
        laybutton.addWidget(self.colormap)
        laybutton.addWidget(self.check_reverse)

        self.disp = rayDisplay(vel,x,y,float(self.vmin.text()),float(self.vmax.text()),self.colormap.currentText())
        self.tbar = NavigationToolbar(self.disp,self)
        self.mainLayout.addLayout(laybutton)
        self.mainLayout.addWidget(self.disp)
        self.mainLayout.addWidget(self.tbar)

    def view_click(self):
        cmap = ''
        if self.check_reverse.isChecked() == False:
            cmap = self.colormap.currentText()
        else:
            cmap = str(self.colormap.currentText()+'_r')
        self.mainLayout.removeWidget(self.disp)
        self.mainLayout.removeWidget(self.tbar)
        sip.delete(self.disp)
        sip.delete(self.tbar)
        self.disp = None
        self.tbar = None
        self.disp = rayDisplay(self.vel, self.x, self.y, float(self.vmin.text()), float(self.vmax.text()),
                               cmap)
        self.tbar = NavigationToolbar(self.disp, self)
        self.mainLayout.addWidget(self.disp)
        self.mainLayout.addWidget(self.tbar)


class mainTabRayDisplay(QWidget):
    def __init__(self, parent = None):
        super(mainTabRayDisplay, self).__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.mainTab = QTabWidget()
        self.mainTab.setTabsClosable(True)
        self.mainTab.tabCloseRequested.connect(self.closeTab)
        self.setLayout(self.mainLayout)

        self.searchLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.searchLayout)
        self.mainLayout.addWidget(self.mainTab)
        self.lineVel2d = QLineEdit()
        self.lineVel2d.setPlaceholderText('2D Velocity (*.vel2d) path')

        buttonVel2d = QPushButton()
        buttonVel2d.setText('...')
        buttonVel2d.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonVel2d.clicked.connect(self.clickButtonVel2d)

        # self.lineRay = QLineEdit()
        # self.lineRay.setPlaceholderText('Ray (*.ray2d) path')
        #
        # buttonRay = QPushButton()
        # buttonRay.setText('...')
        # buttonRay.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # buttonRay.clicked.connect(self.clickButtonRay)

        buttonExecute = QPushButton()
        buttonExecute.setText('View')
        buttonExecute.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonExecute.clicked.connect(self.clickButtonExecute)

        self.searchLayout.addWidget(self.lineVel2d)
        self.searchLayout.addWidget(buttonVel2d)
        # self.searchLayout.addWidget(self.lineRay)
        # self.searchLayout.addWidget(buttonRay)
        self.searchLayout.addWidget(buttonExecute)


    def clickButtonVel2d(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open 2D velocity file', '/', "Format File (*.vel2d)")
        self.lineVel2d.setText(filepath[0])

    def clickButtonRay(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open ray resolution file', '/', "Format File (*.ray2d)")
        self.lineRay.setText(filepath[0])

    def clickButtonExecute(self):
        dir, fil1 = os.path.split(self.lineVel2d.text())
        # dir, fil2 = os.path.split(self.lineRay.text())

        main = mainRayDisplay(self.lineVel2d.text())
        self.mainTab.addTab(main,fil1)

    def closeTab (self, currentIndex):
        currentQWidget = self.mainTab.widget(currentIndex)
        currentQWidget.deleteLater()
        self.mainTab.removeTab(currentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rayfile = 'D:\Testing\Anlyze2D/fwd/rayfile2.ray2d'
    velfile = 'D:\Testing\Anlyze2D/fwd/velocity.vel2d'
    # main = mainRayDisplay(velfile)
    main = mainTabRayDisplay()
    main.show()
    sys.exit(app.exec_())