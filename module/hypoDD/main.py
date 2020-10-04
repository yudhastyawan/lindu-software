import sys
import subprocess
import shutil
import numpy as np
import os
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from module.hypoDD.subroutine.bmkg2pha import bmkg2pha
from module.hypoDD.subroutine.ph2dt_inp import ph2t_inp
from module.hypoDD.subroutine.hypoDD_inp import hypoDD_inp

from mpl_toolkits.basemap import Basemap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

from subroutine.thread.threading import Worker, MessageBox, MessageOpt
from subroutine.time.tictac import tic, tac

class QT5MplCanvas2(FigureCanvas):
    def __init__(self,filename,parent):
        rms = self.extract(filename)

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)

        # file = np.genfromtxt("D:/notepad\jhd-vel.txt")
        # v1 = file[:, 0]
        # v2 = file[:, 1]
        # d = file[:, 2]

        self.axes.set_title('RMS Error (Hist)')
        self.axes.set_ylabel('N Event')
        self.axes.set_xlabel('RMS')
        self.axes.hist(rms, bins=5, color='blue')
        # g = data
        # data = data[:,:,int(np.fix(n*(len(Z)-1)/np.max(Z)))]

        #------------------------
        # m = Basemap(width=((lon.max()-lon.min())*111194.9266),height=((lat.max()-lat.min())*111194.9266),projection='aeqd', lat_0=lat.mean(), lon_0=lon.mean(), ax=self.axes)
        # # fill background.
        # m.drawmapboundary(fill_color='aqua')
        # # draw coasts and fill continents.
        # m.drawcoastlines(linewidth=0.5)
        # m.fillcontinents(color='coral', lake_color='aqua')
        # # draw parallels.
        # parallels = np.arange(lat.min(), lat.max(), np.round((lat.max()-lat.min())*0.1,5))
        # m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=5)
        # # draw meridians
        # meridians = np.arange(lon.min(), lon.max(), np.round((lon.max()-lon.min())*0.1,5))
        # m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=5)
        # # draw a black dot at the center.
        # x,y = m(lon,lat)
        # m.plot(x, y, 'ro')
        # #------------------------
        #
        # self.axes2 = self.fig.add_subplot(122,projection='3d')
        # self.axes2.set_title('Location of Event')
        # self.axes2.set_ylabel('Latitude')
        # self.axes2.set_xlabel('Longitude')
        # self.axes2.set_zlabel('Depth (km)')
        # # #
        #
        FigureCanvas.__init__(self, self.fig)
        # Axes3D.mouse_init(self.axes2)
        # self.axes2.scatter(lat,lon,depth,color='red')
        # # #
        # self.axes2.set_zlim((np.max(depth), np.min(depth)))
        #
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def extract(self,filename):
        file = open(filename, 'r')
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].split()
        file.close()

        rms = []
        for i in range(len(data)):
            rms.append(float(data[i][-2]))
        rms = np.array(rms)
        return rms

class QT5MplCanvas(FigureCanvas):
    def __init__(self,data,parent):
        lat = np.zeros((len(data),1))
        lon = np.zeros((len(data),1))
        depth = np.zeros((len(data),1))

        for i in range(len(data)):
            lat[i] = data[i][1]
            lon[i] = data[i][2]
            depth[i] = data[i][3]

        self.fig = Figure()
        self.axes = self.fig.add_subplot(121)
        self.axes.set_title('Location of Event')
        self.axes.set_ylabel('Latitude')
        self.axes.set_xlabel('Longitude')
        # g = data
        # data = data[:,:,int(np.fix(n*(len(Z)-1)/np.max(Z)))]

        #------------------------
        m = Basemap(width=((lon.max()-lon.min())*111194.9266),height=((lat.max()-lat.min())*111194.9266),projection='aeqd', lat_0=lat.mean(), lon_0=lon.mean(), ax=self.axes)
        # fill background.
        m.drawmapboundary(fill_color='aqua')
        # draw coasts and fill continents.
        m.drawcoastlines(linewidth=0.5)
        m.fillcontinents(color='coral', lake_color='aqua')
        # draw parallels.
        # parallels = np.arange(-90, 90, np.ceil((lat.max()-lat.min())/10))
        parallels = np.arange(lat.min(), lat.max(), np.round((lat.max() - lat.min()) * 0.1, 5))
        m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=5)
        # draw meridians
        # meridians = np.arange(0, 360, np.ceil((lon.max()-lon.min())/10))
        meridians = np.arange(lon.min(), lon.max(), np.round((lon.max() - lon.min()) * 0.1, 5))
        m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=5)
        # draw a black dot at the center.
        x,y = m(lon,lat)
        m.plot(x, y, 'ro')
        #------------------------

        self.axes2 = self.fig.add_subplot(122,projection='3d')
        self.axes2.set_title('Location of Event')
        self.axes2.set_ylabel('Latitude')
        self.axes2.set_xlabel('Longitude')
        self.axes2.set_zlabel('Depth (km)')
        # #

        FigureCanvas.__init__(self, self.fig)
        Axes3D.mouse_init(self.axes2)
        self.axes2.scatter(lat,lon,depth,color='red')
        # #
        self.axes2.set_zlim((np.max(depth), np.min(depth)))

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # create path user
        self.direc = os.getcwd()
        self.enginespath = os.path.join(os.getcwd(),'module','hypoDD', 'engine', 'engines-hypoDD')
        self.engineshypoDDexe = os.path.join(os.getcwd(),'module','hypoDD', 'engine', 'hypoDD.exe')
        self.enginesph2dtexe = os.path.join(os.getcwd(),'module','hypoDD', 'engine', 'ph2dt.exe')
        file = open(self.enginespath, 'w')
        file.write(self.engineshypoDDexe+'\n')
        file.write(self.enginesph2dtexe + '\n')
        file.close()

        # design GUI
        self.setWindowTitle('HypoDD')
        self.menubar()
        self.main_widget()
        self.threadpool = QThreadPool()

    # create main widget
    def main_widget(self):
        # build central widget
        form_central = QWidget()

        # build layout of form central
        layout_central = QHBoxLayout()

        # build group for relocating
        group_relocate = QGroupBox()
        group_relocate.setTitle('Relocate DD')
        group_relocate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        self.settings_group_relocate()
        group_relocate.setLayout(self.relocatelayout)

        # build tab for view data
        tab_view = QTabWidget()
        self.tab_data()
        self.tab_view2D()
        tab_view.addTab(self.main_data,"Data")
        tab_view.addTab(self.main_view2D, "View")

        # setting widget to layout
        layout_central.addWidget(group_relocate)
        layout_central.addWidget(tab_view)

        # setting layout to form
        form_central.setLayout(layout_central)

        # making form central to central widget position
        self.setCentralWidget(form_central)

        self.statbar = self.statusBar()
        self.labstat = QLabel()
        self.labstat.setText('status: Nothing')
        self.statbar.addWidget(self.labstat)

    def settings_group_relocate(self):
        # build main layout
        self.relocatelayout = QVBoxLayout()

        #build inout layout
        inout_layout = QHBoxLayout()

        # build group of input data
        group_input_data = QGroupBox()
        group_input_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QFormLayout()

        # -> filled
        self.line_dtcc = QLineEdit()
        self.line_dtcc.setPlaceholderText('Path for cross-corr diff. time input (dt.cc)')
        self.line_dtct = QLineEdit()
        self.line_dtct.setPlaceholderText('Path for dt.ct')
        self.line_eventdatDD = QLineEdit()
        self.line_eventdatDD.setPlaceholderText('Path for event.sel/dat')
        self.line_stationDD = QLineEdit()
        self.line_stationDD.setPlaceholderText('Path for station.dat')
        self.line_vel = QLineEdit()
        self.line_vel.setPlaceholderText('Path for velocity.vel')

        btn_search_dtcc = QPushButton()
        btn_search_dtcc.setText('...')
        btn_search_dtcc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_dtcc.clicked.connect(self.btn_search_dtcc_clicked)
        btn_search_dtct = QPushButton()
        btn_search_dtct.setText('...')
        btn_search_dtct.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_dtct.clicked.connect(self.btn_search_dtct_clicked)
        btn_search_eventdatDD = QPushButton()
        btn_search_eventdatDD.setText('...')
        btn_search_eventdatDD.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_eventdatDD.clicked.connect(self.btn_search_eventdatDD_clicked)
        btn_search_stationDD = QPushButton()
        btn_search_stationDD.setText('...')
        btn_search_stationDD.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_stationDD.clicked.connect(self.btn_search_stationDD_clicked)
        btn_search_vel = QPushButton()
        btn_search_vel.setText('...')
        btn_search_vel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_vel.clicked.connect(self.btn_search_vel_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_dtcc, btn_search_dtcc)
        layout_input_data.addRow(self.line_dtct, btn_search_dtct)
        layout_input_data.addRow(self.line_eventdatDD, btn_search_eventdatDD)
        layout_input_data.addRow(self.line_stationDD, btn_search_stationDD)
        layout_input_data.addRow(self.line_vel, btn_search_vel)
        group_input_data.setLayout(layout_input_data)
        inout_layout.addWidget(group_input_data)
        self.relocatelayout.addLayout(inout_layout)

        # build group of parameters
        group_parameters = QGroupBox()
        group_parameters.setTitle('Settings of Parameters')
        layout_parameters = QFormLayout()

        # -> filled
        # --> data selection
        lb_idat = QLabel()
        lb_idat.setText('Data type')
        lb_idat.setToolTip('1 = cross correlation data only; 2 = absolute (catalog) data only; 3 = x-corr & catalog.')
        self.idat = QLineEdit()
        self.idat.setText('2')

        lb_ipha = QLabel()
        lb_ipha.setText('Phase Type')
        lb_ipha.setToolTip('1 = P-wave; 2 = S-wave; 3 = P-& S-wave')
        self.ipha = QLineEdit()
        self.ipha.setText('1')

        lb_dist = QLabel()
        lb_dist.setText('Max. distance between centroid of event cluster and stations (km)')
        lb_dist.setToolTip('Max. distance between centroid of event cluster and stations')
        self.dist = QLineEdit()
        self.dist.setText('200')

        # --> event clustering
        lb_obscc = QLabel()
        lb_obscc.setText('Min. number of x-corr links')
        lb_obscc.setToolTip('Min. number of x-corr links per event pair to form a continuous cluster. 0 = no clustering performed. If IDAT = 3, the sum of OBSCC and OBSCT is taken and used for both.')
        self.obscc = QLineEdit()
        self.obscc.setText('0')

        lb_obsct = QLabel()
        lb_obsct.setText('Min. number of catalog links')
        lb_obsct.setToolTip('Min. number of catalog links per event pair to form a continuous cluster. 0 = no clustering performed. If IDAT = 3, the sum of OBSCC and OBSCT is taken and used for both.')
        self.obsct = QLineEdit()
        self.obsct.setText('8')

        # --> solution control
        lb_istart = QLabel()
        lb_istart.setText('Initial locations')
        lb_istart.setToolTip('1 = start from cluster centroid; 2 = start from catalog locations')
        self.istart = QLineEdit()
        self.istart.setText('2')

        lb_isolv = QLabel()
        lb_isolv.setText('Least squares solution')
        lb_isolv.setToolTip('1 = singular value decomposition (SVD); 2 = conjugate gradients (LSQR).')
        self.isolv = QLineEdit()
        self.isolv.setText('1')

        lb_cid = QLabel()
        lb_cid.setText('Index of cluster to be relocated')
        lb_cid.setToolTip('Index of cluster to be relocated (0 = all)')
        self.cid = QLineEdit()
        self.cid.setText('0')

        lb_vpvs = QLabel()
        lb_vpvs.setText('vp/vs ratio')
        lb_vpvs.setToolTip('This ratio is constant for all layers')
        self.vpvs = QLineEdit()
        self.vpvs.setText('1.75')

        # -> settings to layout
        layout_parameters.addRow(lb_idat, self.idat)
        layout_parameters.addRow(lb_ipha, self.ipha)
        layout_parameters.addRow(lb_dist, self.dist)
        layout_parameters.addRow(lb_obscc, self.obscc)
        layout_parameters.addRow(lb_obsct, self.obsct)
        layout_parameters.addRow(lb_istart, self.istart)
        layout_parameters.addRow(lb_isolv, self.isolv)
        layout_parameters.addRow(lb_cid, self.cid)
        layout_parameters.addRow(lb_vpvs, self.vpvs)
        group_parameters.setLayout(layout_parameters)
        self.relocatelayout.addWidget(group_parameters)

        # build group of output data
        group_output_data = QGroupBox()
        group_output_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QFormLayout()

        # -> filled
        self.line_hypoDDloc = QLineEdit()
        self.line_hypoDDloc.setPlaceholderText('Path for hypoDD.loc')
        self.line_hypoDDreloc = QLineEdit()
        self.line_hypoDDreloc.setPlaceholderText('Path for hypoDD.reloc')
        self.line_hypoDDsta = QLineEdit()
        self.line_hypoDDsta.setPlaceholderText('Path for hypoDD.sta')
        self.line_hypoDDres = QLineEdit()
        self.line_hypoDDres.setPlaceholderText('Path for hypoDD.res')
        self.line_hypoDDsrc = QLineEdit()
        self.line_hypoDDsrc.setPlaceholderText('Path for hypoDD.src')

        btn_search_hypoDDloc = QPushButton()
        btn_search_hypoDDloc.setText('...')
        btn_search_hypoDDloc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDDloc.clicked.connect(self.btn_search_hypoDDloc_clicked)
        btn_search_hypoDDreloc = QPushButton()
        btn_search_hypoDDreloc.setText('...')
        btn_search_hypoDDreloc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDDreloc.clicked.connect(self.btn_search_hypoDDreloc_clicked)
        btn_search_hypoDDsta = QPushButton()
        btn_search_hypoDDsta.setText('...')
        btn_search_hypoDDsta.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDDsta.clicked.connect(self.btn_search_hypoDDsta_clicked)
        btn_search_hypoDDres = QPushButton()
        btn_search_hypoDDres.setText('...')
        btn_search_hypoDDres.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDDres.clicked.connect(self.btn_search_hypoDDres_clicked)
        btn_search_hypoDDsrc = QPushButton()
        btn_search_hypoDDsrc.setText('...')
        btn_search_hypoDDsrc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDDsrc.clicked.connect(self.btn_search_hypoDDsrc_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_hypoDDloc, btn_search_hypoDDloc)
        layout_output_data.addRow(self.line_hypoDDreloc, btn_search_hypoDDreloc)
        layout_output_data.addRow(self.line_hypoDDsta, btn_search_hypoDDsta)
        layout_output_data.addRow(self.line_hypoDDres, btn_search_hypoDDres)
        layout_output_data.addRow(self.line_hypoDDsrc, btn_search_hypoDDsrc)
        group_output_data.setLayout(layout_output_data)
        inout_layout.addWidget(group_output_data)

        # build group of data weighting and reweighting
        group_weight = QGroupBox()
        group_weight.setTitle('Path of Data Weighting and Reweighting')
        layout_weight = QVBoxLayout()

        # -> filled
        layout_nset = QHBoxLayout()

        lb_nset = QLabel()
        lb_nset.setText('Number of sets of iteration')
        lb_nset.setToolTip('Number of sets of iteration specifications following')
        self.nset = QLineEdit()
        self.nset.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.nset.setText('')

        self.table_weighting = QTableWidget()
        self.table_weighting.setColumnCount(10)
        self.table_weighting.setHorizontalHeaderLabels(["NITER","WTCCP","WTCCS","WRCC","WDCC","WTCTP","WTCTS","WRCT","WDCT","DAMP"])

        # set of tooltips headers
        self.table_weighting.horizontalHeaderItem(0).setToolTip("Number of iterations for the set of weighting parameters that follow")
        self.table_weighting.horizontalHeaderItem(1).setToolTip(
            "Weight for cross-corr P-wave data. –9 = data not used.")
        self.table_weighting.horizontalHeaderItem(2).setToolTip(
            "Weight for cross-corr S-wave data. –9 = data not used.")
        self.table_weighting.horizontalHeaderItem(3).setToolTip(
            "Weight for catalog P-wave data. –9 = data not used.")
        self.table_weighting.horizontalHeaderItem(4).setToolTip(
            "Weight for catalog S-wave data. –9 = data not used.")
        self.table_weighting.horizontalHeaderItem(5).setToolTip(
            "Cutoff threshold for outliers located on the tails of the cross-corr. 0<1 = absolute threshold in sec (static cutoff). ≥1 = factor to multiply standard deviation (dynamic cutoff). -9 = no outlier removed.")
        self.table_weighting.horizontalHeaderItem(6).setToolTip(
            "Cutoff threshold for outliers located on the tails of the catalog data. 0<1 = absolute threshold in sec (static cutoff). ≥1 = factor to multiply standard deviation (dynamic cutoff). -9 = no outlier removed.")
        self.table_weighting.horizontalHeaderItem(7).setToolTip(
            "Max. event separation distance [km] for x-corr data. -9 = not activated.")
        self.table_weighting.horizontalHeaderItem(8).setToolTip(
            "Max. event separation distance [km] for catalog data. -9 = not activated.")
        self.table_weighting.horizontalHeaderItem(9).setToolTip(
            "Damping (only for Least squares solution = 2 (Conjungate Gradients)).")

        btn_enter_nset = QPushButton()
        btn_enter_nset.setText('->')
        btn_enter_nset.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_enter_nset.clicked.connect(self.act_enter_nset)

        # -> settings to layout
        layout_nset.addWidget(lb_nset)
        layout_nset.addWidget(self.nset)
        layout_nset.addWidget(btn_enter_nset)
        layout_weight.addLayout(layout_nset)
        layout_weight.addWidget(self.table_weighting)
        group_weight.setLayout(layout_weight)
        self.relocatelayout.addWidget(group_weight)

        # build of button execute and cancel
        btn_settings_ok = QPushButton()
        btn_settings_ok.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn_settings_ok.setText('Relocate!')
        btn_settings_ok.clicked.connect(self.btn_relocate_ok_clicked)

        # -> settings to layout
        okcancel_layout = QHBoxLayout()
        okcancel_layout.addWidget(btn_settings_ok)
        self.relocatelayout.addLayout(okcancel_layout)

    def execute_this_btn_relocate_ok_clicked(self, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()

        # open from file user
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_hypoDD, fil = os.path.split(self.user_engine[0])
        drive, pathfil = os.path.splitdrive(self.user_engine[0])

        weight = np.zeros((int(self.nset.text()), 10))
        for i in range(int(self.nset.text())):
            for j in range(10):
                weight[i, j] = self.table_weighting.item(i, j).text()

        file = open(self.line_vel.text(), 'r')
        vel = file.readlines()
        for i in range(len(vel)):
            vel[i] = vel[i].split()
        file.close()

        hypoDD_inp(os.path.join(self.path_hypoDD,'hypoDD.inp'), self.line_dtcc.text(), self.line_dtct.text(),
                   self.line_eventdatDD.text(), self.line_stationDD.text(), self.line_hypoDDloc.text(),
                   self.line_hypoDDreloc.text(),
                   self.line_hypoDDsta.text(), self.line_hypoDDres.text(), self.line_hypoDDsrc.text(), self.idat.text(),
                   self.ipha.text(),
                   self.dist.text(), self.obscc.text(), self.obsct.text(), self.istart.text(), self.isolv.text(),
                   self.nset.text(), self.cid.text(),
                   weight, self.vpvs.text(), vel)
        file = open(os.path.join(self.path_hypoDD,'hypoDD.bat'), 'w')
        file.write(
            drive + '\n' +
            'cd ' + self.path_hypoDD + '\n' +
            'hypoDD hypoDD.inp'
        )
        file.close()
        process = subprocess.Popen(os.path.join(self.path_hypoDD,'hypoDD.bat'), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        progress_callback.emit(str(process.communicate()[0].decode('utf-8',errors='ignore')))
        elt = tac()
        return elt

    def btn_relocate_ok_clicked_output(self, s):
        elaps = 'Elapsed Time:' + '\t' + s + '\n'
        self.message = MessageOpt('Finished','Elapsed Time',elaps)
        self.message.show()

    def btn_relocate_ok_clicked_complete(self):
        self.labstat.setText('Status: Finished')

    def progress_btn_relocate_ok_clicked(self, n):
        self.cmd = QMainWindow()
        # self.cmd.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.cmd.setWindowTitle('process log')
        self.cmd.resize(500,500)
        text = QTextEdit()
        text.setAcceptRichText(True)
        text.append(n)
        self.cmd.setCentralWidget(text)
        self.cmd.show()

        self.labstat.setText(n)

    def btn_relocate_ok_clicked_error(self):
        self.message = MessageBox()
        self.message.show()

    def btn_relocate_ok_clicked(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_btn_relocate_ok_clicked)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.btn_relocate_ok_clicked_output)
        worker.signals.error.connect(self.btn_relocate_ok_clicked_error)
        worker.signals.finished.connect(self.btn_relocate_ok_clicked_complete)
        worker.signals.progress.connect(self.progress_btn_relocate_ok_clicked)

        # Execute
        self.threadpool.start(worker)

    def btn_search_dtcc_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open dt.cc file', '/', "Format File (*.cc)")
        self.line_dtcc.setText(filepath[0])

    def btn_search_dtct_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open dt.ct file', '/', "Format File (*.ct)")
        self.line_dtct.setText(filepath[0])

    def btn_search_eventdatDD_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open event file', '/', "Format File (*.dat *.sel)")
        self.line_eventdatDD.setText(filepath[0])

    def btn_search_stationDD_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station file', '/', "Format File (*.dat)")
        self.line_stationDD.setText(filepath[0])

    def btn_search_vel_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velocity file', '/', "Format File (*.vel)")
        self.line_vel.setText(filepath[0])

    def btn_search_hypoDDloc_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypoDD.loc file', '/', "Format File (*.loc)")
        self.line_hypoDDloc.setText(filepath[0])

    def btn_search_hypoDDreloc_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypoDD.reloc file', '/', "Format File (*.reloc)")
        self.line_hypoDDreloc.setText(filepath[0])

    def btn_search_hypoDDsta_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypoDD.sta file', '/', "Format File (*.sta)")
        self.line_hypoDDsta.setText(filepath[0])

    def btn_search_hypoDDres_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypoDD.res file', '/', "Format File (*.res)")
        self.line_hypoDDres.setText(filepath[0])

    def btn_search_hypoDDsrc_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypoDD.src file', '/', "Format File (*.src)")
        self.line_hypoDDsrc.setText(filepath[0])

    def act_enter_nset(self):
        self.table_weighting.setRowCount(int(self.nset.text()))

    def closeTab_tabel (self, currentIndex):
        currentQWidget = self.tab_tabel.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tab_tabel.removeTab(currentIndex)

    def tab_data(self):
        self.main_data = QWidget()
        self.data_layout = QVBoxLayout()
        self.tab_tabel = QTabWidget()
        self.tab_tabel.setTabsClosable(True)
        self.tab_tabel.tabCloseRequested.connect(self.closeTab_tabel)

        # path
        # -> build upper layout
        path_layout = QHBoxLayout()

        # -> filled
        self.line_data = QLineEdit()
        self.line_data.setPlaceholderText('path of data (all file format)')
        btn_search_data = QPushButton()
        btn_search_data.setText('...')
        btn_search_data.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_data.clicked.connect(self.btn_search_data_clicked)

        btn_enter_data = QPushButton()
        btn_enter_data.setText('View!')
        btn_enter_data.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_enter_data.clicked.connect(self.btn_enter_data_clicked)

        # -> input to layout
        path_layout.addWidget(self.line_data)
        path_layout.addWidget(btn_search_data)
        path_layout.addWidget(btn_enter_data)
        self.data_layout.addLayout(path_layout)
        self.data_layout.addWidget(self.tab_tabel)

        # input layout to widget
        self.main_data.setLayout(self.data_layout)

    def btn_search_data_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open file', '/', "Format File (*.*)")
        self.line_data.setText(filepath[0])

    def btn_enter_data_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()
        file = open(self.line_data.text(), 'r')
        viewit = file.readlines()
        for i in range(len(viewit)):
            viewit[i] = viewit[i].split()
        file.close()

        # view
        tabel = QTableWidget()
        tabel.setRowCount(len(viewit))
        tabel.setColumnCount(len(viewit[0][:]))

        for i in range(len(viewit)):
            for j in range(len(viewit[0][:])):
                tabel.setItem(i,j,QTableWidgetItem(viewit[i][j]))

        graph_layout.addWidget(tabel)
        graph_widget.setLayout(graph_layout)
        dir, fil = os.path.split(self.line_data.text())
        self.tab_tabel.addTab(graph_widget,fil)

    def closeTab (self, currentIndex):
        currentQWidget = self.tab_graph.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tab_graph.removeTab(currentIndex)

    def tab_view2D(self):
        self.main_view2D = QWidget()
        self.view_layout = QVBoxLayout()
        self.tab_graph = QTabWidget()
        self.tab_graph.setTabsClosable(True)
        self.tab_graph.tabCloseRequested.connect(self.closeTab)

        # path
        # -> build upper layout
        path_layout = QHBoxLayout()

        # -> filled
        self.line_view = QLineEdit()
        self.line_view.setPlaceholderText('path of hypoDD.loc or hypoDD.reloc')
        btn_search_view = QPushButton()
        btn_search_view.setText('...')
        btn_search_view.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn_search_view.clicked.connect(self.btn_search_view_clicked)

        btn_enter_view = QPushButton()
        btn_enter_view.setText('View!')
        btn_enter_view.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_enter_view.clicked.connect(self.btn_enter_view_clicked)

        # -> input to layout
        path_layout.addWidget(self.line_view)
        path_layout.addWidget(btn_search_view)
        path_layout.addWidget(btn_enter_view)
        self.view_layout.addLayout(path_layout)
        self.view_layout.addWidget(self.tab_graph)

        # input layout to widget
        self.main_view2D.setLayout(self.view_layout)

    def btn_search_view_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open hypoDD.loc or .reloc file', '/', "Format File (*.loc *.reloc)")
        self.line_view.setText(filepath[0])

    def btn_enter_view_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()
        file = open(self.line_view.text(), 'r')
        viewit = file.readlines()
        for i in range(len(viewit)):
            viewit[i] = viewit[i].split()
        file.close()


        # canvas view
        # -> build canvas
        qmc = QT5MplCanvas(viewit,self.main_view2D)
        ntb = NavigationToolbar(qmc, self.main_view2D)

        # -> input to layout
        graph_layout.addWidget(qmc)
        graph_layout.addWidget(ntb)

        graph_widget.setLayout(graph_layout)
        dir, fil = os.path.split(self.line_view.text())
        self.tab_graph.addTab(graph_widget,fil)

    def btn_search_viewvel_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open hypoDD.reloc file', '/', "Format File (*.reloc)")
        self.line_viewvel.setText(filepath[0])

    def btn_enter_viewvel_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()
        # file = open(self.line_view.text(), 'r')
        # viewit = file.readlines()
        # for i in range(len(viewit)):
        #     viewit[i] = viewit[i].split()
        # file.close()


        # canvas view
        # -> build canvas
        qmc = QT5MplCanvas2(self.line_viewvel.text(),self.velform)
        ntb = NavigationToolbar(qmc, self.velform)
        #
        # # -> input to layout
        graph_layout.addWidget(qmc)
        graph_layout.addWidget(ntb)
        #
        graph_widget.setLayout(graph_layout)
        dir, fil = os.path.split(self.line_viewvel.text())
        self.tab_graphvel.addTab(graph_widget,fil)

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.convert = self.mbar.addMenu('Convert')
        self.bmkg2pha = self.convert.addAction('BMKG to PHA')
        self.ph2dt = self.convert.addAction('PHA to DT/SEL')
        self.settings = self.mbar.addAction('Settings')
        self.analysis = self.mbar.addMenu('Analysis')
        self.rms = self.analysis.addAction('Hist RMS Error')
        self.help = self.mbar.addAction('Help')

        # add signal and slot to menubar
        self.bmkg2pha.triggered.connect(self.act_bmkg2pha)
        self.rms.triggered.connect(self.act_rmsmodel)
        self.ph2dt.triggered.connect(self.act_ph2dt)
        self.settings.triggered.connect(self.act_settings)

    def act_rmsmodel(self):
        # self.velform = QMainWindow()
        self.velform = QWidget()
        self.velform.setWindowTitle('Hist RMS Error')
        self.velform.setMinimumHeight(600)
        self.velform.setMinimumWidth(600)
        self.view_layoutvel = QVBoxLayout()
        self.tab_graphvel = QTabWidget()
        self.tab_graphvel.setTabsClosable(True)
        self.tab_graphvel.tabCloseRequested.connect(self.closeTab)

        # path
        # -> build upper layout
        path_layout = QHBoxLayout()

        # -> filled
        self.line_viewvel = QLineEdit()
        self.line_viewvel.setPlaceholderText('path of *.reloc')
        btn_search_viewvel = QPushButton()
        btn_search_viewvel.setText('...')
        btn_search_viewvel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_viewvel.clicked.connect(self.btn_search_viewvel_clicked)

        btn_enter_view = QPushButton()
        btn_enter_view.setText('View!')
        btn_enter_view.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_enter_view.clicked.connect(self.btn_enter_viewvel_clicked)

        # -> input to layout
        path_layout.addWidget(self.line_viewvel)
        path_layout.addWidget(btn_search_viewvel)
        path_layout.addWidget(btn_enter_view)
        self.view_layoutvel.addLayout(path_layout)
        self.view_layoutvel.addWidget(self.tab_graphvel)

        # input layout to widget
        self.velform.setLayout(self.view_layoutvel)
        self.velform.show()

    # action of bmkg2pha
    def act_bmkg2pha(self):
        # build form ph2dt
        self.form_bmkg2pha = QMainWindow()
        mainwidget = QWidget(self.form_bmkg2pha)
        self.form_bmkg2pha.setWindowTitle('Wizard BMKG buletin to PHA')
        # self.form_bmkg2pha.setWindowFlag(Qt.WindowStaysOnTopHint)

        # build main layout
        mainlayout = QVBoxLayout()

        # build group of input data
        group_input_data = QGroupBox()
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QFormLayout()

        # -> filled
        self.line_BMKG = QLineEdit()
        self.line_BMKG.setPlaceholderText('Path for BMKG buletin (*.*')

        btn_search_BMKG = QPushButton()
        btn_search_BMKG.setText('...')
        btn_search_BMKG.clicked.connect(self.btn_search_BMKG_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_BMKG, btn_search_BMKG)
        group_input_data.setLayout(layout_input_data)
        mainlayout.addWidget(group_input_data)

        # build group of output data
        group_output_data = QGroupBox()
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QFormLayout()

        # -> filled
        self.line_pha = QLineEdit()
        self.line_pha.setPlaceholderText('Path for output .pha')

        btn_search_pha = QPushButton()
        btn_search_pha.setText('...')
        btn_search_pha.clicked.connect(self.btn_search_pha_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_pha, btn_search_pha)
        group_output_data.setLayout(layout_output_data)
        mainlayout.addWidget(group_output_data)

        # build of button execute and cancel
        btn_settings_ok = QPushButton()
        btn_settings_ok.setText('OK')
        btn_settings_ok.clicked.connect(self.btn_bmkg2pha_ok_clicked)
        btn_settings_cancel = QPushButton()
        btn_settings_cancel.setText('Cancel')
        btn_settings_cancel.clicked.connect(self.btn_bmkg2pha_cancel_clicked)

        # -> settings to layout
        okcancel_layout = QHBoxLayout()
        okcancel_layout.addWidget(btn_settings_ok)
        okcancel_layout.addWidget(btn_settings_cancel)
        mainlayout.addLayout(okcancel_layout)

        # setting layouts to form
        mainwidget.setLayout(mainlayout)
        self.form_bmkg2pha.setCentralWidget(mainwidget)

        # show form bmkg2pha
        self.form_bmkg2pha.show()

    # back end of bmkg2pha
    def btn_search_BMKG_clicked(self):
        open = QFileDialog()
        bmkg_filepath = open.getOpenFileName(self, 'Open BMKG file', '/',"Format File (*.*)")
        self.line_BMKG.setText(bmkg_filepath[0])

    def btn_search_pha_clicked(self):
        save = QFileDialog()
        pha_filepath = save.getSaveFileName(self, 'Save PHA file', '/',"Format File (*.pha)")
        self.line_pha.setText(pha_filepath[0])

    def btn_bmkg2pha_ok_clicked(self):
        bmkg2pha(self.line_BMKG.text(),self.line_pha.text())
        self.form_bmkg2pha.close()

    def btn_bmkg2pha_cancel_clicked(self):
        self.form_bmkg2pha.close()

    # action of ph2dt
    def act_ph2dt(self):
        # build form ph2dt
        self.form_ph2dt = QMainWindow()
        mainwidget = QWidget(self.form_ph2dt)
        self.form_ph2dt.setWindowTitle('Wizard PHA to DT/SEL')

        # build main layout
        mainlayout = QVBoxLayout()

        # build group of input data
        group_input_data = QGroupBox()
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QFormLayout()

        # -> filled
        self.line_station = QLineEdit()
        self.line_station.setPlaceholderText('Path for station.dat')
        self.line_phase = QLineEdit()
        self.line_phase.setPlaceholderText('Path for phase.dat/.pha')

        btn_search_station = QPushButton()
        btn_search_station.setText('...')
        btn_search_station.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn_search_station.clicked.connect(self.btn_search_station_clicked)
        btn_search_phase = QPushButton()
        btn_search_phase.setText('...')
        btn_search_phase.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn_search_phase.clicked.connect(self.btn_search_phase_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_station,btn_search_station)
        layout_input_data.addRow(self.line_phase,btn_search_phase)
        group_input_data.setLayout(layout_input_data)
        mainlayout.addWidget(group_input_data)

        # build group of parameters
        group_parameters = QGroupBox()
        group_parameters.setTitle('Settings of Parameters')
        layout_parameters = QFormLayout()

        # -> filled
        lb_minwght = QLabel()
        lb_minwght.setText('Minimum pick weight (0-1)')
        lb_minwght.setToolTip('Note that weights less than 10^(-5) are not considered in hypoDD')
        self.minwght = QLineEdit()
        self.minwght.setText('0')

        lb_maxdist = QLabel()
        lb_maxdist.setText('Maximum distance (km)')
        lb_maxdist.setToolTip('between event pair and station')
        self.maxdist = QLineEdit()
        self.maxdist.setText('500')

        lb_maxsep = QLabel()
        lb_maxsep.setText('Max. hypocentral separation (km)')
        lb_maxsep.setToolTip('between event pairs')
        self.maxsep = QLineEdit()
        self.maxsep.setText('10')

        lb_maxngh = QLabel()
        lb_maxngh.setText('Max. number of neighbors per event')
        lb_maxngh.setToolTip('Max. number of neighbors per event')
        self.maxngh = QLineEdit()
        self.maxngh.setText('10')

        lb_minlnk = QLabel()
        lb_minlnk.setText('Min. number of links')
        lb_minlnk.setToolTip('required to define a neighbor')
        self.minlnk = QLineEdit()
        self.minlnk.setText('8')

        lb_minobs = QLabel()
        lb_minobs.setText('Min. number observations')
        lb_minobs.setToolTip('Min. number of links per pair saved')
        self.minobs = QLineEdit()
        self.minobs.setText('8')

        lb_maxobs = QLabel()
        lb_maxobs.setText('Max. number observations')
        lb_maxobs.setToolTip('Max. number of links per pair saved (ordered by distance from event pair)')
        self.maxobs = QLineEdit()
        self.maxobs.setText('50')

        # -> settings to layout
        layout_parameters.addRow(lb_minwght, self.minwght)
        layout_parameters.addRow(lb_maxdist, self.maxdist)
        layout_parameters.addRow(lb_maxsep, self.maxsep)
        layout_parameters.addRow(lb_maxngh, self.maxngh)
        layout_parameters.addRow(lb_minlnk, self.minlnk)
        layout_parameters.addRow(lb_minobs, self.minobs)
        layout_parameters.addRow(lb_maxobs, self.maxobs)
        group_parameters.setLayout(layout_parameters)
        mainlayout.addWidget(group_parameters)

        # build group of output data
        group_output_data = QGroupBox()
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QFormLayout()

        # -> filled
        self.line_dt = QLineEdit()
        self.line_dt.setPlaceholderText('Path for output dt.ct')
        self.line_eventdat = QLineEdit()
        self.line_eventdat.setPlaceholderText('Path for output event.dat')
        self.line_eventsel = QLineEdit()
        self.line_eventsel.setPlaceholderText('Path for output event.sel')

        btn_search_dt = QPushButton()
        btn_search_dt.setText('...')
        btn_search_dt.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_dt.clicked.connect(self.btn_search_dt_clicked)
        btn_search_eventdat = QPushButton()
        btn_search_eventdat.setText('...')
        btn_search_eventdat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_eventdat.clicked.connect(self.btn_search_eventdat_clicked)
        btn_search_eventsel = QPushButton()
        btn_search_eventsel.setText('...')
        btn_search_eventsel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_eventsel.clicked.connect(self.btn_search_eventsel_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_dt,btn_search_dt)
        layout_output_data.addRow(self.line_eventdat,btn_search_eventdat)
        layout_output_data.addRow(self.line_eventsel, btn_search_eventsel)
        group_output_data.setLayout(layout_output_data)
        mainlayout.addWidget(group_output_data)

        # build of button execute and cancel
        btn_settings_ok = QPushButton()
        btn_settings_ok.setText('OK')
        btn_settings_ok.clicked.connect(self.btn_ph2dt_ok_clicked)
        btn_settings_cancel = QPushButton()
        btn_settings_cancel.setText('Cancel')
        btn_settings_cancel.clicked.connect(self.btn_ph2dt_cancel_clicked)

        # -> settings to layout
        okcancel_layout = QHBoxLayout()
        okcancel_layout.addWidget(btn_settings_ok)
        okcancel_layout.addWidget(btn_settings_cancel)
        mainlayout.addLayout(okcancel_layout)

        # setting layouts to form
        mainwidget.setLayout(mainlayout)
        self.form_ph2dt.setCentralWidget(mainwidget)

        # show form ph2dt
        self.form_ph2dt.show()

    def execute_this_btn_ph2dt_ok_clicked(self, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()

        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_ph2dt, fil = os.path.split(self.user_engine[1])
        drive, pathfil = os.path.splitdrive(self.user_engine[1])

        ph2t_inp(os.path.join(self.path_ph2dt, 'ph2dt.inp'), self.line_station.text(), self.line_phase.text(),
                 self.minwght.text(), self.maxdist.text(),
                 self.maxsep.text(), self.maxngh.text(), self.minlnk.text(), self.minobs.text(), self.maxobs.text())
        file = open(os.path.join(self.path_ph2dt, 'ph2dt.bat'), 'w')
        file.write(
            drive + '\n' +
            'cd ' + self.path_ph2dt + '\n' +
            'ph2dt ph2dt.inp'
        )
        file.close()
        process = subprocess.Popen(os.path.join(self.path_ph2dt, 'ph2dt.bat'), stderr=subprocess.STDOUT,
                                   stdout=subprocess.PIPE)
        progress_callback.emit(str(process.communicate()[0].decode('utf-8', errors='ignore')))
        elt = tac()
        return elt

    def btn_ph2dt_ok_clicked_output(self, s):
        elaps = 'Elapsed Time:' + '\t' + s + '\n'
        self.message = MessageOpt('Finished', 'Elapsed Time', elaps)
        self.message.show()

    def btn_ph2dt_ok_clicked_complete(self):
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_ph2dt, fil = os.path.split(self.user_engine[1])

        shutil.copyfile(os.path.join(self.path_ph2dt, 'dt.ct'), self.line_dt.text())
        shutil.copyfile(os.path.join(self.path_ph2dt, 'event.sel'), self.line_eventsel.text())
        shutil.copyfile(os.path.join(self.path_ph2dt, 'event.dat'), self.line_eventdat.text())
        self.labstat.setText('Status: Finished')

        if os.path.isfile(os.path.join(self.path_ph2dt, 'station.dat')):
            os.remove(os.path.join(self.path_ph2dt, 'station.dat'))
        if os.path.isfile(os.path.join(self.path_ph2dt, 'phase.pha')):
            os.remove(os.path.join(self.path_ph2dt, 'phase.pha'))
        if os.path.isfile(os.path.join(self.path_ph2dt, 'dt.ct')):
            os.remove(os.path.join(self.path_ph2dt, 'dt.ct'))
        if os.path.isfile(os.path.join(self.path_ph2dt, 'event.sel')):
            os.remove(os.path.join(self.path_ph2dt, 'event.sel'))
        if os.path.isfile(os.path.join(self.path_ph2dt, 'event.dat')):
            os.remove(os.path.join(self.path_ph2dt, 'event.dat'))

    def progress_btn_ph2dt_ok_clicked(self, n):
        self.cmd = QMainWindow()
        # self.cmd.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.cmd.setWindowTitle('process log')
        self.cmd.resize(500, 500)
        text = QTextEdit()
        text.setAcceptRichText(True)
        text.append(n)
        self.cmd.setCentralWidget(text)
        self.cmd.show()

        self.labstat.setText(n)

    def btn_ph2dt_ok_clicked_error(self):
        self.message = MessageBox()
        self.message.show()

    def btn_ph2dt_ok_clicked(self):
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_ph2dt, fil = os.path.split(self.user_engine[1])

        shutil.copyfile(self.line_station.text(), os.path.join(self.path_ph2dt, 'station.dat'))
        shutil.copyfile(self.line_phase.text(), os.path.join(self.path_ph2dt, 'phase.pha'))
        # Pass the function to execute
        worker = Worker(
            self.execute_this_btn_ph2dt_ok_clicked)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.btn_ph2dt_ok_clicked_output)
        worker.signals.error.connect(self.btn_ph2dt_ok_clicked_error)
        worker.signals.finished.connect(self.btn_ph2dt_ok_clicked_complete)
        worker.signals.progress.connect(self.progress_btn_ph2dt_ok_clicked)

        # Execute
        self.threadpool.start(worker)

    def btn_ph2dt_cancel_clicked(self):
        self.form_ph2dt.close()

    def btn_search_station_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station.dat', '/', "Format File (*.dat)")
        self.line_station.setText(filepath[0])

    def btn_search_phase_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open phase.dat/.pha', '/', "Format File (*.dat *.pha)")
        self.line_phase.setText(filepath[0])

    def btn_search_dt_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save dt.ct', '/', "Format File (*.ct)")
        self.line_dt.setText(filepath[0])

    def btn_search_eventsel_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save event.sel', '/', "Format File (*.sel)")
        self.line_eventsel.setText(filepath[0])

    def btn_search_eventdat_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save event.dat', '/', "Format File (*.dat)")
        self.line_eventdat.setText(filepath[0])

    # action of settings
    def act_settings(self):
        # open from file user
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()

        self.form_settings = QMainWindow()
        # self.form_settings.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.form_settings.setWindowTitle('Settings')
        self.tab_settings = QTabWidget()
        self.tab_set_engines()
        self.tab_settings.addTab(self.form_engines,'Engines')
        self.form_settings.setCentralWidget(self.tab_settings)
        self.form_settings.show()

    # action tab settings engines
    def tab_set_engines(self):

        # build form engines to create tab settings
        self.form_engines = QWidget()
        self.form_engines.setWindowTitle('Engines')

        # build main layout for tab engines
        mainlayout = QVBoxLayout()
        okeandcancel_layout = QHBoxLayout()

        # build grup of open open directory engines
        groupfile = QGroupBox()
        groupfile.setTitle('Path of Engines')
        layout_groupfile = QFormLayout()

        # build group filled
        self.line_hypoDD = QLineEdit()
        self.line_hypoDD.setPlaceholderText('Path for hypoDD.exe')
        self.line_hypoDD.setText(str(self.user_engine[0]))
        # self.path_hypoDD = path(str(self.user_engine[0]))
        self.line_ph2dt = QLineEdit()
        self.line_ph2dt.setPlaceholderText('Path for ph2dt.exe')
        self.line_ph2dt.setText(str(self.user_engine[1]))
        # self.path_ph2dt = path(str(self.user_engine[2]))

        btn_search_hypoDD = QPushButton()
        btn_search_hypoDD.setText('...')
        btn_search_hypoDD.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDD.clicked.connect(self.btn_search_hypoDD_clicked)
        btn_search_ph2dt = QPushButton()
        btn_search_ph2dt.setText('...')
        btn_search_ph2dt.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_ph2dt.clicked.connect(self.btn_search_ph2dt_clicked)

        # build ok and cancel button
        btn_settings_ok = QPushButton()
        btn_settings_ok.setText('Apply')
        btn_settings_ok.clicked.connect(self.btn_engines_ok_clicked)
        btn_settings_cancel = QPushButton()
        btn_settings_cancel.setText('Cancel')
        btn_settings_cancel.clicked.connect(self.btn_engines_cancel_clicked)

        # settings layout to form
        okeandcancel_layout.addWidget(btn_settings_ok)
        okeandcancel_layout.addWidget(btn_settings_cancel)
        layout_groupfile.addRow(self.line_hypoDD,btn_search_hypoDD)
        layout_groupfile.addRow(self.line_ph2dt,btn_search_ph2dt)
        groupfile.setLayout(layout_groupfile)
        mainlayout.addWidget(groupfile)
        mainlayout.addLayout(okeandcancel_layout)
        self.form_engines.setLayout(mainlayout)

    def btn_search_hypoDD_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open hypoDD.exe', 'hypoDD', "Format File (*.exe)")
        self.line_hypoDD.setText(filepath[0])

    def btn_search_ph2dt_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open ph2dt.exe', 'ph2dt', "Format File (*.exe)")
        # self.path_ph2dt = filepath[0]
        self.line_ph2dt.setText(filepath[0])

    def btn_engines_ok_clicked(self):
        file = open(self.enginespath, 'w')
        file.write(str(self.line_hypoDD.text())+'\n')
        file.write(str(self.line_ph2dt.text()))
        self.form_settings.close()

    def btn_engines_cancel_clicked(self):
        self.form_settings.close()

# execute by system
if __name__ == '__main__':
    App = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(App.exec_())