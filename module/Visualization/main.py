import sys
import obspy as ob
import os
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from subroutine.thread.threading import Worker, MessageBox, MessageOpt
from subroutine.time.tictac import tic, tac
from module.Visualization.subroutine.pyqtEditable import *

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

class QT5MplCanvas(FigureCanvas):
    def __init__(self, path, parent = None):
        data = ob.read(path)
        n = data.count()

        with plt.rc_context({'axes.edgecolor':'white','xtick.color':'white','ytick.color':'white'}):
            self.fig = Figure()
            self.fig.patch.set_facecolor((0,0,0))
            self.ax = self.fig.subplots(n,1,sharex=True)
            self.fig.tight_layout()
            self.fig.subplots_adjust(wspace=0, hspace=0)

            for i in range(n):
                tr = data.pop(0)
                x = tr.data
                t = tr.times('matplotlib')
                self.ax[i].plot(t,x,'r')
                self.ax[i].set_facecolor((0,0,0))

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # create temp file save
        self.tempfile = ''
        self.idxfile = []

        # create path user
        self.direc = os.getcwd()
        self.enginespath = os.path.join(os.getcwd(),'module','Visualization', 'engine', 'seismopath')
        file = open(self.enginespath, 'w')
        file.close()

        # design GUI
        self.setWindowTitle('Visualization')
        self.menubar()
        self.main_widget()
        self.threadpool = QThreadPool()

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.file = self.mbar.addMenu('File')
        self.loaddata = self.file.addAction('Load Data')
        self.help = self.mbar.addAction('Help')

        self.loaddata.triggered.connect(self.act_loaddata)

    def main_widget(self):
        self.main_tab = QTabWidget()
        self.main_tab.setTabsClosable(True)
        self.main_tab.tabCloseRequested.connect(self.close_maintab)
        self.main_tab.currentChanged.connect(self.tabChanged)
        self.main_tab.tabBarClicked.connect(self.tabChanged)

        self.setCentralWidget(self.main_tab)

        self.statbar = self.statusBar()
        self.labstat = QLabel()
        self.labstat.setText('status: Nothing')
        self.statbar.addWidget(self.labstat)


    def act_loaddata_execute(self, path, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()

        data = ob.read(path)
        self.idxfile.append(path)
        self.tempfile = path

        n = data.count()
        self.nn = n
        file = open(self.enginespath,'a')
        for i in range(n):
            file.write(
                'i' + '\t' + path + '\n'
            )
        file.close()
        elt = tac()
        return elt

    def act_loaddata_output(self, s):
        elaps = 'Elapsed Time:' + '\t' + s + '\n'
        self.message = MessageOpt('Finished','Elapsed Time',elaps)
        self.message.show()

    def act_loaddata_complete(self):
        self.labstat.setText('Status: Finished')
        self.graphdat(self.filepath,self.nn)

    def act_loaddata_progress(self, n):
        self.labstat.setText(n)

    def act_loaddata_error(self):
        self.message = MessageBox()
        self.message.show()

    def act_loaddata(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open seismogram file', '/', "Format File (*.*)")

        if filepath[0] != '':
            self.filepath = filepath[0]
            # Pass the function to execute
            worker = Worker(self.act_loaddata_execute,filepath[0])
            # worker.signals.result.connect(self.act_loaddata_output)
            worker.signals.error.connect(self.act_loaddata_error)
            worker.signals.finished.connect(self.act_loaddata_complete)
            worker.signals.progress.connect(self.act_loaddata_progress)

            # Execute
            self.threadpool.start(worker)

    def graphdat(self, path, n):
        graph_wid = QTabWidget()
        dir, fil = os.path.split(path)
        self.main_tab.addTab(graph_wid, fil)

        graph_graph = Scroller()
        graph_graph.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        graph_graph_wid = QWidget()
        graph_graph_wid.setAutoFillBackground(True)
        graph_graph_wid.setStyleSheet("background-color: black")
        graph_graph_wid.setMinimumHeight(QDesktopWidget().screenGeometry().height()*np.ceil(n/3))
        graph_graph_wid.setMinimumWidth(QDesktopWidget().screenGeometry().width())


        graph_graph_view = QT5MplCanvas(path)
        graph_graph_toolbar = QToolBar()
        graph_graph_toolbar.addAction('Filter')
        graph_graph_toolbar.addAction('Pick')
        graph_graph_toolbar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        graph_graph_lay = QVBoxLayout()
        graph_graph_lay.addWidget(graph_graph_toolbar)
        graph_graph_lay.addWidget(graph_graph_view)
        # graph_graph_lay.SetFixedSize(QSize(10000000,1000))
        graph_graph_wid.setLayout(graph_graph_lay)

        graph_graph.setWidget(graph_graph_wid)
        graph_data = QWidget()
        graph_wid.addTab(graph_graph, 'Graph')
        graph_wid.addTab(graph_data, 'Data')

    def close_maintab (self, currentIndex):
        a = self.tempfile
        currentQWidget = self.main_tab.widget(currentIndex)
        currentQWidget.deleteLater()
        self.main_tab.removeTab(currentIndex)
        self.idxfile.remove(self.idxfile[currentIndex])
        self.tempfile = a

    def tabChanged(self, i):
        self.tempfile = self.idxfile[i]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())