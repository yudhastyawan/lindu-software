import sys
import subprocess
import shutil
import numpy as np
import os
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from modules.JHD.subroutine.velest_cmn import velest_cmn

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
        v1,v2,d = self.extract(filename)

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)

        line_up, = self.axes.step(v1, d, '--')
        line_down, = self.axes.step(v2, d, '-')
        self.axes.legend([line_up, line_down], ['velocity (init)', 'velocity (JHD)'])
        self.axes.set_title('JHD Velocity Update')
        self.axes.set_ylabel('depth (km)')
        self.axes.set_xlabel('velocity (km/s)')
        self.axes.set_ylim(d.max(), d.min())

        FigureCanvas.__init__(self, self.fig)

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

        v0 = []
        v1 = []
        d = []
        for i in range(len(data)):
            if data[i] != [] and data[i][0] == 'layer':
                k = i + 1
                while data[k] != []:
                    v0.append(float(data[k][1]))
                    d.append(float(data[k][2]))
                    k = k + 1
            if data[i] != [] and data[i][0] == 'nlay':
                k = i + 2
                while data[k] != []:
                    if data[k][3] == 'km':
                        v1.append(float(data[k][4]))
                    else:
                        v1.append(float(data[k][3]))
                    k = k + 1
        v0 = np.array(v0)
        v1 = np.array(v1)
        d = np.array(d)
        return v0,v1,d

class QT5MplCanvas(FigureCanvas):
    def __init__(self,filename,parent):
        lat,lon,depth = self.extract(filename)

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
        parallels = np.arange(lat.min(), lat.max(), np.round((lat.max()-lat.min())*0.1,5))
        m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=5)
        # draw meridians
        meridians = np.arange(lon.min(), lon.max(), np.round((lon.max()-lon.min())*0.1,5))
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

    def extract(self, filename):
        file = open(filename, 'r')
        data = file.readlines()
        for i in range(data.__len__()):
            data[i] = data[i].split()
        file.close()
        lat = []
        lon = []
        depth = []
        for i in range(data.__len__()):
            if data[i] != [] and (
                    data[i][0][0] == '1' or
                    data[i][0][0] == '2' or
                    data[i][0][0] == '3' or
                    data[i][0][0] == '4' or
                    data[i][0][0] == '5' or
                    data[i][0][0] == '6' or
                    data[i][0][0] == '7' or
                    data[i][0][0] == '8' or
                    data[i][0][0] == '9' or
                    data[i][0][0] == '0'
            ):
                if data[i][-6][-1] == 'N':
                    lat.append(float(data[i][-6][0:7]))
                else:
                    lat.append(-1 * float(data[i][-6][0:7]))
                if data[i][-5][-1] == 'E':
                    lon.append(float(data[i][-5][0:8]))
                else:
                    lon.append(-1 * float(data[i][-5][0:8]))
                depth.append(float(data[i][-4]))

        lat = np.array(lat)
        lon = np.array(lon)
        depth = np.array(depth)

        return lat,lon,depth


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # create path user
        self.direc = os.getcwd()
        self.enginespath = os.path.join(os.getcwd(),'module','JHD', 'engine', 'engines-jhd')
        self.enginesexe = os.path.join(os.getcwd(),'module','JHD', 'engine', 'velest.exe')
        file = open(self.enginespath, 'w')
        file.write(self.enginesexe)
        file.close()

        # design GUI
        self.setWindowTitle('JHD')
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
        group_locate = QGroupBox()
        group_locate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        group_relocate = QWidget()
        group_locate.setTitle('Locate JHD')
        group_relocate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        self.settings_group_relocate()
        group_relocate.setLayout(self.relocatelayout)
        locate_layout = QVBoxLayout()
        group_locate.setLayout(locate_layout)

        # scroll
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        scroll.setWidgetResizable(False)
        scroll.setWidget(group_relocate)
        locate_layout.addWidget(scroll)
        layout_central.addWidget(group_locate)

        # build tab for view data
        tab_view = QTabWidget()
        self.tab_data()
        self.tab_view2D()
        tab_view.addTab(self.main_data,"Data")
        tab_view.addTab(self.main_view2D, "View")

        # setting widget to layout
        # layout_central.addWidget(group_relocate)
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
        group_input_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QFormLayout()

        # -> filled
        self.line_modelfile = QLineEdit()
        self.line_modelfile.setPlaceholderText('Path for model file (*.mod)')
        self.line_statfile = QLineEdit()
        self.line_statfile.setPlaceholderText('Path for station file (*.sta)')
        self.line_quake = QLineEdit()
        self.line_quake.setPlaceholderText('Path for earthquake data (*.cnv/.sed/.arcvel')
        self.line_regnames = QLineEdit()
        self.line_regnames.setPlaceholderText('Path for region names (*.dat)')
        self.line_regcoor = QLineEdit()
        self.line_regcoor.setPlaceholderText('Path for region coordinates (*.dat)')
        self.line_seisfile = QLineEdit()
        self.line_seisfile.setPlaceholderText('Path for seismo-file (*.param)')

        btn_search_modelfile = QPushButton()
        btn_search_modelfile.setText('...')
        btn_search_modelfile.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_modelfile.clicked.connect(self.btn_search_modelfile_clicked)
        btn_search_statfile = QPushButton()
        btn_search_statfile.setText('...')
        btn_search_statfile.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_statfile.clicked.connect(self.btn_search_statfile_clicked)
        btn_search_quake = QPushButton()
        btn_search_quake.setText('...')
        btn_search_quake.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_quake.clicked.connect(self.btn_search_quake_clicked)
        btn_search_regnames = QPushButton()
        btn_search_regnames.setText('...')
        btn_search_regnames.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_regnames.clicked.connect(self.btn_search_regnames_clicked)
        btn_search_regcoor = QPushButton()
        btn_search_regcoor.setText('...')
        btn_search_regcoor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_regcoor.clicked.connect(self.btn_search_regcoor_clicked)
        btn_search_seisfile = QPushButton()
        btn_search_seisfile.setText('...')
        btn_search_seisfile.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_seisfile.clicked.connect(self.btn_search_seisfile_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_modelfile, btn_search_modelfile)
        layout_input_data.addRow(self.line_statfile, btn_search_statfile)
        layout_input_data.addRow(self.line_quake, btn_search_quake)
        layout_input_data.addRow(self.line_regnames, btn_search_regnames)
        layout_input_data.addRow(self.line_regcoor, btn_search_regcoor)
        layout_input_data.addRow(self.line_seisfile, btn_search_seisfile)
        group_input_data.setLayout(layout_input_data)
        inout_layout.addWidget(group_input_data)
        self.relocatelayout.addLayout(inout_layout)

        # build group of parameters
        group_parameters = QGroupBox()
        group_parameters.setTitle('Settings of Parameters')
        layout_parameters = QFormLayout()

        # -> filled
        lb_olat = QLabel()
        lb_olat.setText('Latitude (in degrees)')
        lb_olat.setToolTip('Latitude (in degrees)')
        self.olat = QLineEdit()
        self.olat.setText('')

        lb_olon = QLabel()
        lb_olon.setText('Longitude (in degrees)')
        lb_olon.setToolTip('Longitude (in degrees)')
        self.olon = QLineEdit()
        self.olon.setText('')

        lb_rotate = QLabel()
        lb_rotate.setText('Rotate')
        lb_rotate.setToolTip('denotes the angle of clockwise rotated y-axis from North.')
        self.rotate = QLineEdit()
        self.rotate.setText('')

        lb_coordsys = QLabel()
        lb_coordsys.setText('Coordinate system')
        lb_coordsys.setToolTip('= 0 for short distance conversion to cartesian coordinate system all over the Earth with positive values representing Longitude West'+'\n'+
                               '= 1 for short distance conversion to cartesian coordi-nate system all over the Earth with positive values representing Longitude East'+'\n'+
                               '= 2 for Swiss coordinate system Latitudes and Longitudes are used throughout the program (and its input/output) in decimal-degrees')
        self.coordsys = QLineEdit()
        self.coordsys.setText('0')

        lb_zshift = QLabel()
        lb_zshift.setText('Z-shift')
        lb_zshift.setToolTip('is used to systematically shift all hypocenters in depth relative to the depth given in their summary cards')
        self.zshift = QLineEdit()
        self.zshift.setText('0.0')

        lb_itrial = QLabel()
        lb_itrial.setText('Itrial')
        lb_itrial.setToolTip('Controling the trial hypocenter in the single_event_mode'+'\n'+
                             '= 0 use hypocenter coordinates provided by summary card'+'\n'+
                             '= 1 trial hypocenter equals station coordinates of earliest observation and ztrial for depth')
        self.itrial = QLineEdit()
        self.itrial.setText('0')

        lb_ztrial = QLabel()
        lb_ztrial.setText('Ztrial')
        lb_ztrial.setToolTip('Controling the trial hypocenter in the single_event_mode')
        self.ztrial = QLineEdit()
        self.ztrial.setText('0.0')

        lb_ised = QLabel()
        lb_ised.setText('Input format of the earthquake data')
        lb_ised.setToolTip('Controling the input format of the earthquake data'+'\n'+
                           '= 0 in converted (*.CNV) archive format'+'\n'+
                           '= 1 VELEST archive type format'+'\n'+
                           '= 2 SED format (SED= Swiss Seismological Service)')
        self.ised = QLineEdit()
        self.ised.setText('0')

        lb_neq = QLabel()
        lb_neq.setText('Number of earthquakes')
        lb_neq.setToolTip('Number of earthquakes')
        self.neq = QLineEdit()
        self.neq.setText('')

        lb_neq = QLabel()
        lb_neq.setText('Number of earthquakes')
        lb_neq.setToolTip('Number of earthquakes')
        self.neq = QLineEdit()
        self.neq.setText('')

        lb_nshot = QLabel()
        lb_nshot.setText('Number of shots or blasts')
        lb_nshot.setToolTip('Number of shots or blasts')
        self.nshot = QLineEdit()
        self.nshot.setText('')

        lb_isingle = QLabel()
        lb_isingle.setText('Switch controling mode')
        lb_isingle.setToolTip('=0 simultaneous mode'+'\n'+
                              '=1 single_event_mode')
        self.isingle = QLineEdit()
        self.isingle.setText('0')

        lb_iresolcalc = QLabel()
        lb_iresolcalc.setText('Resolution matrix calculation in single_event_mode')
        lb_iresolcalc.setToolTip('Resolution matrix calculation in single_event_mode')
        self.iresolcalc = QLineEdit()
        self.iresolcalc.setText('0')

        lb_dmax = QLabel()
        lb_dmax.setText('Maximal epicentral distance for use of phase')
        lb_dmax.setToolTip('Observations at stations at greater distances are neglected')
        self.dmax = QLineEdit()
        self.dmax.setText('200.0')

        lb_itopo = QLabel()
        lb_itopo.setText('Itopo')
        lb_itopo.setToolTip('= 0 no topographic array is used'+'\n'+
                            '= 1 zmin is set automatically to the topographic height at this point (surface)'+'\n'+
                            '= 2 each raypoint is checked whether it is below the surface or not'+'\n'+
                            '= 3 (and icoordsystem=2): For epicentral distances < 10 km the first and last ray-segment are each splitted into four subsegments')
        self.itopo = QLineEdit()
        self.itopo.setText('0')

        lb_zmin = QLabel()
        lb_zmin.setText('Minimal depth for hypocenters')
        lb_zmin.setToolTip("Used to avoid 'air quakes'")
        self.zmin = QLineEdit()
        self.zmin.setText('0.0')

        lb_veladj = QLabel()
        lb_veladj.setText('Maximal adjustement of layer velocity in each iteration step')
        lb_veladj.setToolTip('Maximal adjustement of layer velocity in each iteration step')
        self.veladj = QLineEdit()
        self.veladj.setText('0.2')

        lb_zadj = QLabel()
        lb_zadj.setText('Maximal adjustement of hypocentral depth in each iteration step')
        lb_zadj.setToolTip('Maximal adjustement of hypocentral depth in each iteration steps')
        self.zadj = QLineEdit()
        self.zadj.setText('5.0')

        lb_lowveloclay = QLabel()
        lb_lowveloclay.setText('low-velocity-layers')
        lb_lowveloclay.setToolTip('=0 no low-velocity layers will result from velocity-inversion'+'\n'+
                                  '=1 low-velocity-channels may result')
        self.lowveloclay = QLineEdit()
        self.lowveloclay.setText('0')

        lb_nsp = QLabel()
        lb_nsp.setText('NSP')
        lb_nsp.setToolTip('=1 P phases only'+'\n'+
                          '=2 P and S phases'+'\n'+
                          '=3 P-S relative travel time')
        self.nsp = QLineEdit()
        self.nsp.setText('1')

        lb_swtfac = QLabel()
        lb_swtfac.setText('General weighting factor')
        lb_swtfac.setToolTip('General weighting factor for S wave data relative to P wave data of same observation weight')
        self.swtfac = QLineEdit()
        self.swtfac.setText('0.5')

        lb_vpvsrat = QLabel()
        lb_vpvsrat.setText('VpVs ratio')
        lb_vpvsrat.setToolTip('VpVs ratio')
        self.vpvsrat = QLineEdit()
        self.vpvsrat.setText('1.730')

        lb_nmod = QLabel()
        lb_nmod.setText('Number of velocity models')
        lb_nmod.setToolTip('Number of velocity models')
        self.nmod = QLineEdit()
        self.nmod.setText('1')

        lb_othet = QLabel()
        lb_othet.setText('damping of origin-time')
        lb_othet.setToolTip('damping of origin-time')
        self.othet = QLineEdit()
        self.othet.setText('0.01')

        lb_xythet = QLabel()
        lb_xythet.setText('damping of horizontal hypocentral coordinates')
        lb_xythet.setToolTip('damping of horizontal hypocentral coordinates')
        self.xythet = QLineEdit()
        self.xythet.setText('0.01')

        lb_zthet = QLabel()
        lb_zthet.setText('damping of hypocentral depth')
        lb_zthet.setToolTip('damping of hypocentral depth')
        self.zthet= QLineEdit()
        self.zthet.setText('0.01')

        lb_vthet = QLabel()
        lb_vthet.setText('damping of velocity-model')
        lb_vthet.setToolTip('damping of velocity-model')
        self.vthet = QLineEdit()
        self.vthet.setText('1.0')

        lb_stathet = QLabel()
        lb_stathet.setText('damping of station-corrections')
        lb_stathet.setToolTip('damping of station-corrections')
        self.stathet = QLineEdit()
        self.stathet.setText('0.1')

        lb_nsinv = QLabel()
        lb_nsinv.setText('Nsinv')
        lb_nsinv.setToolTip('=0 Do NOT invert for station corrections'+'\n'+
                            '=1 invert for station corrections')
        self.nsinv = QLineEdit()
        self.nsinv.setText('1')

        lb_nshcor = QLabel()
        lb_nshcor.setText('Nshcor')
        lb_nshcor.setToolTip('=0 no shot correction applied'+'\n'+
                             '=1 apply shot corrections')
        self.nshcor = QLineEdit()
        self.nshcor.setText('0')

        lb_nshfix = QLabel()
        lb_nshfix.setText('Nshfix')
        lb_nshfix.setToolTip('=0 Do NOT fix shots'+'\n'+
                             '=1 fix shots')
        self.nshfix = QLineEdit()
        self.nshfix.setText('0')

        lb_iuseelev = QLabel()
        lb_iuseelev.setText('Using station elevation')
        lb_iuseelev.setToolTip('=0 station-elevations are NOT used (assumed all equal zero = sea level)')
        self.iuseelev = QLineEdit()
        self.iuseelev.setText('1')

        lb_iusestacorr = QLabel()
        lb_iusestacorr.setText('station-corrections from input-file')
        lb_iusestacorr.setToolTip('=0 station-corrections from input-file are ignored')
        self.iusestacorr = QLineEdit()
        self.iusestacorr.setText('1')

        lb_iturbo = QLabel()
        lb_iturbo.setText('Iturbo')
        lb_iturbo.setToolTip('=1 OUTPUT files 2,7,11,12,77,78,79 are NOT created'+'\n'+
                             '=0 above (large!) OUTPUT files are created')
        self.iturbo = QLineEdit()
        self.iturbo.setText('1')

        lb_icnvout = QLabel()
        lb_icnvout.setText('Option to create *.CNV file with final hypocenters')
        lb_icnvout.setToolTip('Option to create *.CNV file with final hypocenters')
        self.icnvout = QLineEdit()
        self.icnvout.setText('1')

        lb_istaout = QLabel()
        lb_istaout.setText('Option to create *out.STA file for station list')
        lb_istaout.setToolTip('Option to create *out.STA file for station list with final station corrections')
        self.istaout = QLineEdit()
        self.istaout.setText('1')

        lb_ismpout = QLabel()
        lb_ismpout.setText('Option to create *.SMP file')
        lb_ismpout.setToolTip('Option to create *.SMP file with summary cards of final hypocenters')
        self.ismpout = QLineEdit()
        self.ismpout.setText('0')

        lb_irayout = QLabel()
        lb_irayout.setText('Option to create *.RAY file')
        lb_irayout.setToolTip('Option to create *.RAY file')
        self.irayout = QLineEdit()
        self.irayout.setText('0')

        lb_idrvout = QLabel()
        lb_idrvout.setText('Option to create *.DRV file')
        lb_idrvout.setToolTip('Option to create *.DRV file')
        self.idrvout = QLineEdit()
        self.idrvout.setText('0')

        lb_ialeout = QLabel()
        lb_ialeout.setText('Option to create *.ALE file')
        lb_ialeout.setToolTip('Option to create *.ALE file')
        self.ialeout = QLineEdit()
        self.ialeout.setText('0')

        lb_idspout = QLabel()
        lb_idspout.setText('Option to create *.DSP file')
        lb_idspout.setToolTip('Option to create *.DSP file')
        self.idspout = QLineEdit()
        self.idspout.setText('0')

        lb_irflout = QLabel()
        lb_irflout.setText('Option to create *.RFL file')
        lb_irflout.setToolTip('Option to create *.RFL file')
        self.irflout = QLineEdit()
        self.irflout.setText('0')

        lb_irfrout = QLabel()
        lb_irfrout.setText('Option to create *.RFR file')
        lb_irfrout.setToolTip('Option to create *.RFR file')
        self.irfrout = QLineEdit()
        self.irfrout.setText('0')

        lb_iresout = QLabel()
        lb_iresout.setText('Option to create *.RES file')
        lb_iresout.setToolTip('Option to create *.RES file')
        self.iresout = QLineEdit()
        self.iresout.setText('0')

        lb_delmin = QLabel()
        lb_delmin.setText('Stop criterion iteration')
        lb_delmin.setToolTip('Criterion to stop iteration in single-event-mode')
        self.delmin = QLineEdit()
        self.delmin.setText('0.01')

        lb_ittmax = QLabel()
        lb_ittmax.setText('N iterations')
        lb_ittmax.setToolTip('=0 no iteration is performed, but all statistics are calculated and printed!'+'\n'+
                             '=N N iterations with each consisting of a forward and a full inverse solution are performed'+'\n'+
                             'Default value: 5 to 9')
        self.ittmax = QLineEdit()
        self.ittmax.setText('5')

        lb_invertratio = QLabel()
        lb_invertratio.setText('Invert Ratio')
        lb_invertratio.setToolTip('NumIf INVERTRATIO is set to 2, then every second iteration is an inversion type A. If it is set to 1,then every iteration is of type A.')
        self.invertratio = QLineEdit()
        self.invertratio.setText('1')

        # -> settings to layout
        layout_parameters.addRow(lb_olat, self.olat)
        layout_parameters.addRow(lb_olon, self.olon)
        layout_parameters.addRow(lb_rotate, self.rotate)
        layout_parameters.addRow(lb_coordsys, self.coordsys)
        layout_parameters.addRow(lb_zshift, self.zshift)
        layout_parameters.addRow(lb_itrial, self.itrial)
        layout_parameters.addRow(lb_ztrial, self.ztrial)
        layout_parameters.addRow(lb_ised, self.ised)
        layout_parameters.addRow(lb_neq, self.neq)
        layout_parameters.addRow(lb_nshot, self.nshot)
        layout_parameters.addRow(lb_isingle, self.isingle)
        layout_parameters.addRow(lb_iresolcalc, self.iresolcalc)
        layout_parameters.addRow(lb_dmax, self.dmax)
        layout_parameters.addRow(lb_itopo, self.itopo)
        layout_parameters.addRow(lb_zmin, self.zmin)
        layout_parameters.addRow(lb_veladj, self.veladj)
        layout_parameters.addRow(lb_zadj, self.zadj)
        layout_parameters.addRow(lb_lowveloclay, self.lowveloclay)
        layout_parameters.addRow(lb_nsp, self.nsp)
        layout_parameters.addRow(lb_swtfac, self.swtfac)
        layout_parameters.addRow(lb_vpvsrat, self.vpvsrat)
        layout_parameters.addRow(lb_nmod, self.nmod)
        layout_parameters.addRow(lb_othet, self.othet)
        layout_parameters.addRow(lb_xythet, self.xythet)
        layout_parameters.addRow(lb_zthet, self.zthet)
        layout_parameters.addRow(lb_vthet, self.vthet)
        layout_parameters.addRow(lb_stathet, self.stathet)
        layout_parameters.addRow(lb_nsinv, self.nsinv)
        layout_parameters.addRow(lb_nshcor, self.nshcor)
        layout_parameters.addRow(lb_nshfix, self.nshfix)
        layout_parameters.addRow(lb_iuseelev, self.iuseelev)
        layout_parameters.addRow(lb_iusestacorr, self.iusestacorr)
        layout_parameters.addRow(lb_iturbo, self.iturbo)
        layout_parameters.addRow(lb_icnvout, self.icnvout)
        layout_parameters.addRow(lb_istaout, self.istaout)
        layout_parameters.addRow(lb_ismpout, self.ismpout)
        layout_parameters.addRow(lb_irayout, self.irayout)
        layout_parameters.addRow(lb_idrvout, self.idrvout)
        layout_parameters.addRow(lb_ialeout, self.ialeout)
        layout_parameters.addRow(lb_idspout, self.idspout)
        layout_parameters.addRow(lb_irflout, self.irflout)
        layout_parameters.addRow(lb_irfrout, self.irfrout)
        layout_parameters.addRow(lb_iresout, self.iresout)
        layout_parameters.addRow(lb_delmin, self.delmin)
        layout_parameters.addRow(lb_ittmax, self.ittmax)
        layout_parameters.addRow(lb_invertratio, self.invertratio)
        group_parameters.setLayout(layout_parameters)
        self.relocatelayout.addWidget(group_parameters)

        # build group of output data
        group_output_data = QGroupBox()
        group_output_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QFormLayout()

        # -> filled
        self.line_velestout = QLineEdit()
        self.line_velestout.setPlaceholderText('Path for main print-out (*.out)')
        self.line_hypott = QLineEdit()
        self.line_hypott.setPlaceholderText('Path for final hypocenters and traveltimes (*.cnv)')
        self.line_statlist = QLineEdit()
        self.line_statlist.setPlaceholderText('Path for new station list (*.sta)')
        self.line_hypo71 = QLineEdit()
        self.line_hypo71.setPlaceholderText('Path for hypo71 compatible (*.arcvel)')
        self.line_veloutsmp = QLineEdit()
        self.line_veloutsmp.setPlaceholderText('Path for velout.smp')
        self.line_veloutray = QLineEdit()
        self.line_veloutray.setPlaceholderText('Path for velout.ray')
        self.line_veloutdrv = QLineEdit()
        self.line_veloutdrv.setPlaceholderText('Path for velout.drv')
        self.line_veloutale = QLineEdit()
        self.line_veloutale.setPlaceholderText('Path for velout.ale')
        self.line_veloutdspr = QLineEdit()
        self.line_veloutdspr.setPlaceholderText('Path for velout.dspr')
        self.line_veloutrfl = QLineEdit()
        self.line_veloutrfl.setPlaceholderText('Path for velout.rfl')
        self.line_veloutrfr = QLineEdit()
        self.line_veloutrfr.setPlaceholderText('Path for velout.rfr')
        self.line_veloutres = QLineEdit()
        self.line_veloutres.setPlaceholderText('Path for velout.res')

        btn_search_velestout = QPushButton()
        btn_search_velestout.setText('...')
        btn_search_velestout.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_velestout.clicked.connect(self.btn_search_velestout_clicked)
        btn_search_hypott = QPushButton()
        btn_search_hypott.setText('...')
        btn_search_hypott.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypott.clicked.connect(self.btn_search_hypott_clicked)
        btn_search_stalist = QPushButton()
        btn_search_stalist.setText('...')
        btn_search_stalist.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_stalist.clicked.connect(self.btn_search_stalist_clicked)
        btn_search_hypo71 = QPushButton()
        btn_search_hypo71.setText('...')
        btn_search_hypo71.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypo71.clicked.connect(self.btn_search_hypo71_clicked)
        btn_search_veloutsmp = QPushButton()
        btn_search_veloutsmp.setText('...')
        btn_search_veloutsmp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutsmp.clicked.connect(self.btn_search_veloutsmp_clicked)
        btn_search_veloutray = QPushButton()
        btn_search_veloutray.setText('...')
        btn_search_veloutray.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutray.clicked.connect(self.btn_search_veloutray_clicked)
        btn_search_veloutdrv = QPushButton()
        btn_search_veloutdrv.setText('...')
        btn_search_veloutdrv.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutdrv.clicked.connect(self.btn_search_veloutdrv_clicked)
        btn_search_veloutale = QPushButton()
        btn_search_veloutale.setText('...')
        btn_search_veloutale.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutale.clicked.connect(self.btn_search_veloutale_clicked)
        btn_search_veloutdspr = QPushButton()
        btn_search_veloutdspr.setText('...')
        btn_search_veloutdspr.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutdspr.clicked.connect(self.btn_search_veloutdspr_clicked)
        btn_search_veloutrfl = QPushButton()
        btn_search_veloutrfl.setText('...')
        btn_search_veloutrfl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutrfl.clicked.connect(self.btn_search_veloutrfl_clicked)
        btn_search_veloutrfr = QPushButton()
        btn_search_veloutrfr.setText('...')
        btn_search_veloutrfr.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutrfr.clicked.connect(self.btn_search_veloutrfr_clicked)
        btn_search_veloutres = QPushButton()
        btn_search_veloutres.setText('...')
        btn_search_veloutres.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veloutres.clicked.connect(self.btn_search_veloutres_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_velestout, btn_search_velestout)
        layout_output_data.addRow(self.line_statlist, btn_search_stalist)
        layout_output_data.addRow(self.line_hypott, btn_search_hypott)
        layout_output_data.addRow(self.line_hypo71, btn_search_hypo71)
        layout_output_data.addRow(self.line_veloutsmp, btn_search_veloutsmp)
        layout_output_data.addRow(self.line_veloutray, btn_search_veloutray)
        layout_output_data.addRow(self.line_veloutdrv, btn_search_veloutdrv)
        layout_output_data.addRow(self.line_veloutale, btn_search_veloutale)
        layout_output_data.addRow(self.line_veloutdspr, btn_search_veloutdspr)
        layout_output_data.addRow(self.line_veloutrfl, btn_search_veloutrfl)
        layout_output_data.addRow(self.line_veloutrfr, btn_search_veloutrfr)
        layout_output_data.addRow(self.line_veloutres, btn_search_veloutres)
        group_output_data.setLayout(layout_output_data)
        inout_layout.addWidget(group_output_data)

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
        self.path_velest, fil = os.path.split(self.user_engine[0])
        drive, pathfil = os.path.splitdrive(self.user_engine[0])

        velest_cmn(os.path.join(self.path_velest,'velest.cmn'), self.line_modelfile.text(), self.line_statfile.text(),
                   self.line_quake.text(), self.line_regnames.text(),
                   self.line_regcoor.text(), self.line_seisfile.text(), self.olat.text(), self.olon.text(),
                   self.rotate.text(), self.coordsys.text(), self.zshift.text(), self.itrial.text(),
                   self.ztrial.text(), self.ised.text(), self.neq.text(), self.nshot.text(), self.isingle.text(),
                   self.iresolcalc.text(), self.dmax.text(), self.itopo.text(), self.zmin.text(),
                   self.veladj.text(), self.zadj.text(), self.lowveloclay.text(), self.nsp.text(), self.swtfac.text(),
                   self.vpvsrat.text(), self.nmod.text(), self.othet.text(), self.xythet.text(),
                   self.zthet.text(), self.vthet.text(), self.stathet.text(), self.nsinv.text(), self.nshcor.text(),
                   self.nshfix.text(), self.iuseelev.text(), self.iusestacorr.text(),
                   self.iturbo.text(), self.icnvout.text(), self.istaout.text(), self.ismpout.text(),
                   self.irayout.text(), self.idrvout.text(), self.ialeout.text(), self.idspout.text(),
                   self.irflout.text(), self.irfrout.text(), self.iresout.text(), self.delmin.text(),
                   self.ittmax.text(), self.invertratio.text(), self.line_velestout.text(),
                   self.line_statlist.text(), self.line_hypott.text(), self.line_hypo71.text(),
                   self.line_veloutsmp.text(), self.line_veloutray.text(),
                   self.line_veloutdrv.text(), self.line_veloutale.text(), self.line_veloutdspr.text(),
                   self.line_veloutrfl.text(), self.line_veloutrfr.text(),
                   self.line_veloutres.text())

        file = open(os.path.join(self.path_velest,'velest.bat'), 'w')
        file.write(
            drive + '\n' +
            'cd ' + self.path_velest + '\n' +
            'velest velest.cmn'
        )
        file.close()
        process = subprocess.Popen(os.path.join(self.path_velest,'velest.bat'), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
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

    def btn_search_modelfile_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open model file', '/', "Format File (*.mod)")
        self.line_modelfile.setText(filepath[0])

    def btn_search_statfile_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station file', '/', "Format File (*.sta)")
        self.line_statfile.setText(filepath[0])

    def btn_search_quake_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open earhquake data file', '/', "Format File (*.cnv *.sed *.arcvel)")
        self.line_quake.setText(filepath[0])

    def btn_search_regnames_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open region names file', '/', "Format File (*.dat)")
        self.line_regnames.setText(filepath[0])

    def btn_search_regcoor_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open region coordinates file', '/', "Format File (*.dat)")
        self.line_regcoor.setText(filepath[0])

    def btn_search_seisfile_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open seismo-file coordinates file', '/', "Format File (*.param)")
        self.line_seisfile.setText(filepath[0])

    def btn_search_velestout_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save main print-out file', '/', "Format File (*.out)")
        self.line_velestout.setText(filepath[0])

    def btn_search_stalist_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save station list file', '/', "Format File (*.sta)")
        self.line_statlist.setText(filepath[0])

    def btn_search_hypott_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save final hypocenter & traveltime file', '/', "Format File (*.cnv)")
        self.line_hypott.setText(filepath[0])

    def btn_search_hypo71_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save hypo-71 compatible output file', '/', "Format File (*.arcvel)")
        self.line_hypo71.setText(filepath[0])

    def btn_search_veloutsmp_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.smp file', '/', "Format File (*.smp)")
        self.line_veloutsmp.setText(filepath[0])

    def btn_search_veloutray_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.ray file', '/', "Format File (*.ray)")
        self.line_veloutray.setText(filepath[0])

    def btn_search_veloutdrv_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.drv file', '/', "Format File (*.drv)")
        self.line_veloutdrv.setText(filepath[0])

    def btn_search_veloutale_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.ale file', '/', "Format File (*.ale)")
        self.line_veloutale.setText(filepath[0])

    def btn_search_veloutdspr_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.dspr file', '/', "Format File (*.dspr *.dis)")
        self.line_veloutdspr.setText(filepath[0])

    def btn_search_veloutrfl_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.rfl file', '/', "Format File (*.rfl)")
        self.line_veloutrfl.setText(filepath[0])

    def btn_search_veloutrfr_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.rfr file', '/', "Format File (*.rfr)")
        self.line_veloutrfr.setText(filepath[0])

    def btn_search_veloutres_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velout.res file', '/', "Format File (*.res)")
        self.line_veloutres.setText(filepath[0])

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
        viewit = file.read()
        file.close()

        # view
        tabel = QTextEdit()
        tabel.setText(viewit)

        graph_layout.addWidget(tabel)
        graph_widget.setLayout(graph_layout)
        self.tab_tabel.addTab(graph_widget,self.line_data.text().split('/')[-1])

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
        self.line_view.setPlaceholderText('path of *.cnv')
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
        filepath = open.getOpenFileName(self, 'Open velout.cnv file', '/', "Format File (*.cnv)")
        self.line_view.setText(filepath[0])

    def btn_enter_view_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()

        # canvas view
        # -> build canvas
        qmc = QT5MplCanvas(self.line_view.text(),self.main_view2D)
        ntb = NavigationToolbar(qmc, self.main_view2D)

        # -> input to layout
        graph_layout.addWidget(qmc)
        graph_layout.addWidget(ntb)

        graph_widget.setLayout(graph_layout)
        dir, fil = os.path.split(self.line_view.text())
        self.tab_graph.addTab(graph_widget,fil)

    def btn_search_viewvel_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velest.out file', '/', "Format File (*.out)")
        self.line_viewvel.setText(filepath[0])

    def btn_enter_viewvel_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()

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
        self.settings = self.mbar.addAction('Settings')
        self.analysis = self.mbar.addMenu('Analysis')
        self.vel1d = self.analysis.addAction('Plot 1D Vel Model Update')
        self.help = self.mbar.addAction('Help')

        # add signal and slot to menubar
        self.vel1d.triggered.connect(self.act_velmodel)
        self.settings.triggered.connect(self.act_settings)

    def act_velmodel(self):
        # self.velform = QMainWindow()
        self.velform = QWidget()
        self.velform.setWindowTitle('1D Velocity Plot - JHD')
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
        self.line_viewvel.setPlaceholderText('path of *.out')
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
        self.form_settings.setWindowFlag(Qt.WindowStaysOnTopHint)
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
        self.line_hypoDD.setPlaceholderText('Path for velest.exe')
        self.line_hypoDD.setText(str(self.user_engine[0]))

        btn_search_hypoDD = QPushButton()
        btn_search_hypoDD.setText('...')
        btn_search_hypoDD.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_hypoDD.clicked.connect(self.btn_search_hypoDD_clicked)

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
        groupfile.setLayout(layout_groupfile)
        mainlayout.addWidget(groupfile)
        mainlayout.addLayout(okeandcancel_layout)
        self.form_engines.setLayout(mainlayout)

    def btn_search_hypoDD_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velest.exe', 'velest', "Format File (*.exe)")
        self.line_hypoDD.setText(filepath[0])

    def btn_engines_ok_clicked(self):
        file = open(self.enginespath, 'w')
        file.write(str(self.line_hypoDD.text()))
        self.form_settings.close()

    def btn_engines_cancel_clicked(self):
        self.form_settings.close()

# execute by system
if __name__ == '__main__':
    App = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(App.exec_())