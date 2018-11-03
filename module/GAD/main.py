import sys
import subprocess
import shutil
import numpy as np
import os
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

class QT5MplCanvas(FigureCanvas):
    def __init__(self,data,parent):
        lat,lon,depth,rms = self.extract(data)
        # lat = np.zeros((len(data),1))
        # lon = np.zeros((len(data),1))
        # depth = np.zeros((len(data),1))
        #
        # for i in range(len(data)):
        #     lat[i] = data[i][1]
        #     lon[i] = data[i][2]
        #     depth[i] = data[i][3]

        self.fig = Figure()
        gs = GridSpec(1,7)
        self.axes = self.fig.add_subplot(gs[0,0:2], aspect = 'equal')
        self.axes.set_title('Location of Event')
        self.axes.set_ylabel('X')
        self.axes.set_xlabel('Y')
        self.axes.scatter(lat,lon,color='red')
        self.axes.grid()
        # g = data
        # data = data[:,:,int(np.fix(n*(len(Z)-1)/np.max(Z)))]

        #------------------------
        # m = Basemap(width=((lon.max()-lon.min())*111194.9266),height=((lat.max()-lat.min())*111194.9266),projection='aeqd', lat_0=lat.mean(), lon_0=lon.mean(), ax=self.axes)
        # fill background.
        # m.drawmapboundary(fill_color='aqua')
        # draw coasts and fill continents.
        # m.drawcoastlines(linewidth=0.5)
        # m.fillcontinents(color='coral', lake_color='aqua')
        # draw parallels.
        # parallels = np.arange(-90, 90, np.ceil((lat.max()-lat.min())/10))
        # parallels = np.arange(lat.min(), lat.max(), np.round((lat.max() - lat.min()) * 0.1, 5))
        # m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=5)
        # draw meridians
        # meridians = np.arange(0, 360, np.ceil((lon.max()-lon.min())/10))
        # meridians = np.arange(lon.min(), lon.max(), np.round((lon.max() - lon.min()) * 0.1, 5))
        # m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=5)
        # draw a black dot at the center.
        # x,y = m(lon,lat)
        # m.plot(x, y, 'ro')
        #------------------------

        self.axes3 = self.fig.add_subplot(gs[0,-1])
        self.axes3.set_title('RMS Error (Hist)')
        self.axes3.set_ylabel('N Event')
        self.axes3.set_xlabel('RMS')
        self.axes3.hist(rms, bins='auto',color='blue')

        self.axes2 = self.fig.add_subplot(gs[0,3:5],projection='3d')
        self.axes2.set_title('Location of Event')
        self.axes2.set_ylabel('X (km)')
        self.axes2.set_xlabel('Y (km)')
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

    def extract(self,data):
        lat = []
        lon = []
        depth = []
        rms = []
        for i in range(len(data)):
            if data[i] != []:
                if data[i][0] == 'X':
                    lat.append(data[i][1])
                if data[i][0] == 'Y':
                    lon.append(data[i][1])
                if data[i][0] == 'Z':
                    depth.append(data[i][1])
                if data[i][0] == 'Travel' and data[i] != []:
                    rms.append(data[i][-1][0:-4])
        lat = np.array(lat,float)
        lon = np.array(lon,float)
        depth = np.array(depth,float)
        rms = np.array(rms, float)
        return lat,lon,depth,rms

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # create path user
        self.direc = os.getcwd()
        self.enginespath = os.path.join(os.getcwd(),'module','GAD', 'engine', 'engines-gad')
        self.enginesexe = os.path.join(os.getcwd(),'module','GAD', 'engine', 'gad.exe')
        file = open(self.enginespath,'w')
        file.write(self.enginesexe)
        file.close()

        # design GUI
        self.setWindowTitle('GAD')
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
        group_relocate.setTitle('Locate GAD')
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
        group_input_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QFormLayout()

        # -> filled
        self.line_statdat = QLineEdit()
        self.line_statdat.setPlaceholderText('Path for station.dat')
        self.line_veldat = QLineEdit()
        self.line_veldat.setPlaceholderText('Path for velocity.dat')
        self.line_arrdat = QLineEdit()
        self.line_arrdat.setPlaceholderText('Path for arrival.dat')

        btn_search_statdat = QPushButton()
        btn_search_statdat.setText('...')
        btn_search_statdat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_statdat.clicked.connect(self.btn_search_statdat_clicked)
        btn_search_veldat = QPushButton()
        btn_search_veldat.setText('...')
        btn_search_veldat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_veldat.clicked.connect(self.btn_search_veldat_clicked)
        btn_search_arrdat = QPushButton()
        btn_search_arrdat.setText('...')
        btn_search_arrdat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_arrdat.clicked.connect(self.btn_search_arrdat_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_statdat, btn_search_statdat)
        layout_input_data.addRow(self.line_veldat, btn_search_veldat)
        layout_input_data.addRow(self.line_arrdat, btn_search_arrdat)
        group_input_data.setLayout(layout_input_data)
        self.relocatelayout.addWidget(group_input_data)

        # build group of output data
        group_output_data = QGroupBox()
        group_output_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QFormLayout()

        # -> filled
        self.line_resdat = QLineEdit()
        self.line_resdat.setPlaceholderText('Path for result.dat')

        btn_search_resdat = QPushButton()
        btn_search_resdat.setText('...')
        btn_search_resdat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_resdat.clicked.connect(self.btn_search_resdat_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_resdat, btn_search_resdat)
        group_output_data.setLayout(layout_output_data)
        self.relocatelayout.addWidget(group_output_data)

        # build of button execute and cancel
        btn_settings_ok = QPushButton()
        btn_settings_ok.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        btn_settings_ok.setText('Locate!')
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
        self.path_gad, fil = os.path.split(self.user_engine[0])
        drive, pathfil = os.path.splitdrive(self.user_engine[0])

        file = open(os.path.join(self.path_gad,'gad.bat'), 'w')
        file.write(
            drive + '\n' +
            'cd '+ self.path_gad + '\n' +
            'gad.exe'
        )
        file.close()
        process = subprocess.Popen(os.path.join(self.path_gad,'gad.bat'),stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
        progress_callback.emit(str(process.communicate()[0].decode('utf-8',errors='ignore')))

        elt = tac()
        return elt

    def btn_relocate_ok_clicked_output(self, s):
        elaps = 'Elapsed Time:' + '\t' + s + '\n'
        self.message = MessageOpt('Finished','Elapsed Time',elaps)
        self.message.show()

    def btn_relocate_ok_clicked_complete(self):
        # open from file user
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_gad, file = os.path.split(self.user_engine[0])
        shutil.copyfile(os.path.join(self.path_gad, 'Results.dat'), self.line_resdat.text())

        self.labstat.setText('Status: Finished')

        if os.path.isfile(os.path.join(self.path_gad,'station.dat')):
            os.remove(os.path.join(self.path_gad,'station.dat'))
        if os.path.isfile(os.path.join(self.path_gad,'velocity.dat')):
            os.remove(os.path.join(self.path_gad,'velocity.dat'))
        if os.path.isfile(os.path.join(self.path_gad,'arrival.dat')):
            os.remove(os.path.join(self.path_gad,'arrival.dat'))
        if os.path.isfile(os.path.join(self.path_gad, 'Results.dat')):
            os.remove(os.path.join(self.path_gad, 'Results.dat'))

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
        # open from file user
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()
        self.path_gad, file = os.path.split(self.user_engine[0])

        shutil.copyfile(self.line_statdat.text(),os.path.join(self.path_gad,'station.dat'))
        shutil.copyfile(self.line_veldat.text(),os.path.join(self.path_gad,'velocity.dat'))
        shutil.copyfile(self.line_arrdat.text(),os.path.join(self.path_gad,'arrival.dat'))
        # Pass the function to execute
        worker = Worker(self.execute_this_btn_relocate_ok_clicked)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.btn_relocate_ok_clicked_output)
        worker.signals.error.connect(self.btn_relocate_ok_clicked_error)
        worker.signals.finished.connect(self.btn_relocate_ok_clicked_complete)
        worker.signals.progress.connect(self.progress_btn_relocate_ok_clicked)

        # Execute
        self.threadpool.start(worker)

    def btn_search_statdat_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station.dat file', '/', "Format File (*.dat)")
        self.line_statdat.setText(filepath[0])

    def btn_search_veldat_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velocity.dat file', '/', "Format File (*.dat)")
        self.line_veldat.setText(filepath[0])

    def btn_search_arrdat_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open arrival.dat file', '/', "Format File (*.dat)")
        self.line_arrdat.setText(filepath[0])

    def btn_search_resdat_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save result.dat', '/', "Format File (*.dat)")
        self.line_resdat.setText(filepath[0])

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
        viewit = file.read()

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
        self.line_view.setPlaceholderText('path of result.dat')
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
        filepath = open.getOpenFileName(self, 'Open result.dat file', '/', "Format File (*.dat)")
        self.line_view.setText(filepath[0])

    def btn_enter_view_clicked(self):
        graph_widget = QWidget()
        graph_layout = QVBoxLayout()
        file = open(self.line_view.text(), 'r')
        viewit = file.readlines()
        for i in range(len(viewit)):
            viewit[i] = viewit[i].replace('=', ' ')
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
        dir, file = os.path.split(self.line_view.text())
        self.tab_graph.addTab(graph_widget,file)

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.settings = self.mbar.addAction('Settings')
        self.help = self.mbar.addAction('Help')

        self.settings.triggered.connect(self.act_settings)

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
        self.line_gad = QLineEdit()
        self.line_gad.setPlaceholderText('Path for gad.exe')
        self.line_gad.setText(str(self.user_engine[0]))
        # self.path_hypoDD = path(str(self.user_engine[0]))

        btn_search_gad = QPushButton()
        btn_search_gad.setText('...')
        btn_search_gad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_search_gad.clicked.connect(self.btn_search_gad_clicked)

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
        layout_groupfile.addRow(self.line_gad,btn_search_gad)
        groupfile.setLayout(layout_groupfile)
        mainlayout.addWidget(groupfile)
        mainlayout.addLayout(okeandcancel_layout)
        self.form_engines.setLayout(mainlayout)

    def btn_search_gad_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open gad.exe', 'gad', "Format File (*.exe)")
        self.line_hypoDD.setText(filepath[0])

    def btn_engines_ok_clicked(self):
        file = open(self.enginespath, 'w')
        file.write(str(self.line_gad.text()))
        self.form_settings.close()

    def btn_engines_cancel_clicked(self):
        self.form_settings.close()

# execute by system
if __name__ == '__main__':
    App = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(App.exec_())