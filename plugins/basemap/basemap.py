"""
An example of how to use Basemap in pyqt4 application.

Copyright(C) 2011 dbzhang800#gmail.com
"""

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import sys
from pyface.qt import QtGui, QtCore
import os

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mplcanvas = MplCanvas(parent=self)
        self.setCentralWidget(self.mplcanvas)
        self.show()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

        map = Basemap(ax=self.axes)
        map.drawcoastlines()
        map.drawcountries()
        map.drawmapboundary()
        map.fillcontinents(color='coral', lake_color='aqua')
        map.drawmapboundary(fill_color='aqua')

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    # w.show()
    sys.exit(app.exec_())