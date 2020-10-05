import sys
import os
import numpy as np

from pyface.qt import QtGui, QtCore

from module.Tomography.subroutine.tomo_inverse import inversion, inversionS, inversion_test, inversion_testS
from module.Tomography.subroutine.tomo_log import tomo_log, read_log
from subroutine.icon.Icon import icon_tomo
import module.Tomography.subroutine.hypoDD2tomofile as ht
# import module.Tomography.submodule.analyze2D.main as an2d
from subroutine.thread.threading import Worker, MessageBox
from subroutine.time.tictac import tic, tac

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.icon_tab_tg = QtGui.QIcon()
        self.icon_tab_tg.addPixmap(QtGui.QPixmap(icon_tomo), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # design GUI
        self.setWindowTitle('Tomography')
        self.menubar()
        self.main_widget()
        self.threadpool = QtCore.QThreadPool()

    # create main widget
    def main_widget(self):
        # build central widget
        form_central = QtGui.QWidget()

        # build layout of form central
        layout_central = QtGui.QHBoxLayout()

        # build group for relocating
        group_relocate = QtGui.QGroupBox()
        group_relocate.setTitle('Tomography')
        group_relocate.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Expanding)
        self.settings_group_relocate()
        group_relocate.setLayout(self.relocatelayout)

        # setting widget to layout
        layout_central.addWidget(group_relocate)

        # setting layout to form
        form_central.setLayout(layout_central)

        # making form central to central widget position
        self.setCentralWidget(form_central)

        self.statbar = self.statusBar()
        self.labstat = QtGui.QLabel()
        self.labstat.setText('status: Nothing')
        self.statbar.addWidget(self.labstat)

    def settings_group_relocate(self):
        # build main layout
        self.relocatelayout = QtGui.QHBoxLayout()

        #build inout layout
        inout_layout = QtGui.QVBoxLayout()
        velinout_layout = QtGui.QVBoxLayout()

        # build group of input data
        group_input_data = QtGui.QGroupBox()
        group_input_data.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QtGui.QFormLayout()

        # -> filled
        self.line_evtdat = QtGui.QLineEdit()
        self.line_evtdat.setPlaceholderText('Path for event data (*.evt)')
        self.line_statdat = QtGui.QLineEdit()
        self.line_statdat.setPlaceholderText('Path for station data (*.dat)')
        self.line_veldat = QtGui.QLineEdit()
        self.line_veldat.setPlaceholderText('Path for velocity data (*.vel)')

        btn_search_evtdat = QtGui.QPushButton()
        btn_search_evtdat.setText('...')
        btn_search_evtdat.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_evtdat.clicked.connect(self.btn_search_evtdat_clicked)
        btn_search_statdat = QtGui.QPushButton()
        btn_search_statdat.setText('...')
        btn_search_statdat.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_statdat.clicked.connect(self.btn_search_statdat_clicked)
        btn_search_veldat = QtGui.QPushButton()
        btn_search_veldat.setText('...')
        btn_search_veldat.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_veldat.clicked.connect(self.btn_search_veldat_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_evtdat, btn_search_evtdat)
        layout_input_data.addRow(self.line_statdat, btn_search_statdat)
        layout_input_data.addRow(self.line_veldat, btn_search_veldat)
        group_input_data.setLayout(layout_input_data)
        inout_layout.addWidget(group_input_data)
        self.relocatelayout.addLayout(inout_layout)
        self.relocatelayout.addLayout(velinout_layout)

        # build group of parameters
        group_parameters = QtGui.QGroupBox()
        group_parameters.setTitle('Settings of Parameters')
        layout_parameters = QtGui.QFormLayout()

        # -> filled
        # --> data selection
        lb_type = QtGui.QLabel()
        lb_type.setText('Type of Tomography')
        # lb_type.setToolTip('1 = cross correlation data only; 2 = absolute (catalog) data only; 3 = x-corr & catalog.')
        self.type = QtGui.QComboBox()
        self.type.addItem('P')
        self.type.addItem('S')
        self.type.addItem('P & S')

        lb_deg2km = QtGui.QLabel()
        lb_deg2km.setText('degree to km')
        # lb_deg2km.setToolTip('1 = cross correlation data only; 2 = absolute (catalog) data only; 3 = x-corr & catalog.')
        self.deg2km = QtGui.QLineEdit()
        self.deg2km.setText('111')

        lb_nx = QtGui.QLabel()
        lb_nx.setText('Number of X')
        # lb_nx.setToolTip('1 = P-wave; 2 = S-wave; 3 = P-& S-wave')
        self.nx = QtGui.QLineEdit()
        self.nx.setText('10')

        lb_ny = QtGui.QLabel()
        lb_ny.setText('Number of Y')
        # lb_ny.setToolTip('1 = P-wave; 2 = S-wave; 3 = P-& S-wave')
        self.ny = QtGui.QLineEdit()
        self.ny.setText('10')

        lb_nz = QtGui.QLabel()
        lb_nz.setText('Number of Z')
        # lb_nz.setToolTip('1 = P-wave; 2 = S-wave; 3 = P-& S-wave')
        self.nz = QtGui.QLineEdit()
        self.nz.setText('10')

        lb_normd = QtGui.QLabel()
        lb_normd.setText('Norm Value')
        # lb_normd.setToolTip('Max. distance between centroid of event cluster and stations')
        self.normd = QtGui.QLineEdit()
        self.normd.setText('20')

        lb_gradd = QtGui.QLabel()
        lb_gradd.setText('Gradient Value')
        # lb_gradd.setToolTip('Min. number of x-corr links per event pair to form a continuous cluster. 0 = no clustering performed. If IDAT = 3, the sum of OBSCC and OBSCT is taken and used for both.')
        self.gradd = QtGui.QLineEdit()
        self.gradd.setText('20')

        lb_iter = QtGui.QLabel()
        lb_iter.setText('Number of Tomography Iteration')
        # lb_iter.setToolTip('Min. number of catalog links per event pair to form a continuous cluster. 0 = no clustering performed. If IDAT = 3, the sum of OBSCC and OBSCT is taken and used for both.')
        self.iter = QtGui.QLineEdit()
        self.iter.setText('10')

        lb_cacah = QtGui.QLabel()
        lb_cacah.setText('Number of Part of Ray Bending')
        # lb_cacah.setToolTip('1 = start from cluster centroid; 2 = start from catalog locations')
        self.cacah = QtGui.QLineEdit()
        self.cacah.setText('20')

        lb_biter = QtGui.QLabel()
        lb_biter.setText('Number of Ray Iteration')
        # lb_biter.setToolTip('1 = singular value decomposition (SVD); 2 = conjugate gradients (LSQtGui.QR).')
        self.biter = QtGui.QLineEdit()
        self.biter.setText('100')

        lb_split = QtGui.QLabel()
        lb_split.setText('Number of Splitting Ray Resolution')
        # lb_split.setToolTip('Index of cluster to be relocated (0 = all)')
        self.split = QtGui.QLineEdit()
        self.split.setText('100')

        lb_pert = QtGui.QLabel()
        lb_pert.setText('Value of Perturbation Test')
        # lb_pert.setToolTip('Index of cluster to be relocated (0 = all)')
        self.pert = QtGui.QLineEdit()
        self.pert.setText('0.3')

        # -> settings to layout
        layout_parameters.addRow(lb_type, self.type)
        layout_parameters.addRow(lb_deg2km, self.deg2km)
        layout_parameters.addRow(lb_nx, self.nx)
        layout_parameters.addRow(lb_ny, self.ny)
        layout_parameters.addRow(lb_nz, self.nz)
        layout_parameters.addRow(lb_normd, self.normd)
        layout_parameters.addRow(lb_gradd, self.gradd)
        layout_parameters.addRow(lb_iter, self.iter)
        layout_parameters.addRow(lb_cacah, self.cacah)
        layout_parameters.addRow(lb_biter, self.biter)
        layout_parameters.addRow(lb_split, self.split)
        layout_parameters.addRow(lb_pert, self.pert)
        group_parameters.setLayout(layout_parameters)
        self.relocatelayout.addWidget(group_parameters)

        # build group of output data
        group_output_data = QtGui.QGroupBox()
        group_output_data.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        group_output_data.setTitle('Path of Coordinate & Log Output')
        layout_output_data = QtGui.QFormLayout()

        # -> filled
        # self.line_velout = QtGui.QLineEdit()
        # self.line_velout.setPlaceholderText('Path for velocity output (*.vel3d)')
        self.line_xout = QtGui.QLineEdit()
        self.line_xout.setPlaceholderText('Path for x data output (*.data)')
        self.line_yout = QtGui.QLineEdit()
        self.line_yout.setPlaceholderText('Path for y data output (*.data)')
        self.line_zout = QtGui.QLineEdit()
        self.line_zout.setPlaceholderText('Path for z data output (*.data)')
        self.line_velog = QtGui.QLineEdit()
        self.line_velog.setPlaceholderText('Path for log (*.log)')

        # btn_search_velout = QtGui.QPushButton()
        # btn_search_velout.setText('...')
        # btn_search_velout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        # btn_search_velout.clicked.connect(self.btn_search_velout_clicked)
        btn_search_xout = QtGui.QPushButton()
        btn_search_xout.setText('...')
        btn_search_xout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_xout.clicked.connect(self.btn_search_xout_clicked)
        btn_search_yout = QtGui.QPushButton()
        btn_search_yout.setText('...')
        btn_search_yout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_yout.clicked.connect(self.btn_search_yout_clicked)
        btn_search_zout = QtGui.QPushButton()
        btn_search_zout.setText('...')
        btn_search_zout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_zout.clicked.connect(self.btn_search_zout_clicked)
        btn_search_velog = QtGui.QPushButton()
        btn_search_velog.setText('...')
        btn_search_velog.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_velog.clicked.connect(self.btn_search_velog_clicked)

        # -> settings to layout
        # layout_output_data.addRow(self.line_velout, btn_search_velout)
        layout_output_data.addRow(self.line_xout, btn_search_xout)
        layout_output_data.addRow(self.line_yout, btn_search_yout)
        layout_output_data.addRow(self.line_zout, btn_search_zout)
        layout_output_data.addRow(self.line_velog, btn_search_velog)
        group_output_data.setLayout(layout_output_data)
        inout_layout.addWidget(group_output_data)

        # build group of output data
        group_resoutput_data = QtGui.QGroupBox()
        group_resoutput_data.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        group_resoutput_data.setTitle('Path of Test Resolution Output')
        layout_resoutput_data = QtGui.QFormLayout()

        # -> filled
        self.line_velobsout = QtGui.QLineEdit()
        self.line_velobsout.setPlaceholderText('Path for obs velocity output (*.vel3d)')
        self.line_velcalout = QtGui.QLineEdit()
        self.line_velcalout.setPlaceholderText('Path for cal velocity output (*.vel3d)')

        btn_search_velobsout = QtGui.QPushButton()
        btn_search_velobsout.setText('...')
        btn_search_velobsout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        btn_search_velobsout.clicked.connect(self.btn_search_velobsout_clicked)
        btn_search_velcalout = QtGui.QPushButton()
        btn_search_velcalout.setText('...')
        btn_search_velcalout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_velcalout.clicked.connect(self.btn_search_velcalout_clicked)

        # -> settings to layout
        layout_resoutput_data.addRow(self.line_velobsout, btn_search_velobsout)
        layout_resoutput_data.addRow(self.line_velcalout, btn_search_velcalout)
        group_resoutput_data.setLayout(layout_resoutput_data)
        velinout_layout.addWidget(group_resoutput_data)

        # build group of output data
        group_veloutput_data = QtGui.QGroupBox()
        group_veloutput_data.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        group_veloutput_data.setTitle('Path of Velocity Inversion Output')
        layout_veloutput_data = QtGui.QFormLayout()

        # -> filled
        self.line_velpout = QtGui.QLineEdit()
        self.line_velpout.setPlaceholderText('Path for P velocity output (*.vel3d)')
        self.line_velsout = QtGui.QLineEdit()
        self.line_velsout.setPlaceholderText('Path for S velocity output (*.vel3d)')
        self.line_velpsout = QtGui.QLineEdit()
        self.line_velpsout.setPlaceholderText('Path for P/S velocity output (*.vel3d)')

        btn_search_velpout = QtGui.QPushButton()
        btn_search_velpout.setText('...')
        btn_search_velpout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_velpout.clicked.connect(self.btn_search_velpout_clicked)
        btn_search_velsout = QtGui.QPushButton()
        btn_search_velsout.setText('...')
        btn_search_velsout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_velsout.clicked.connect(self.btn_search_velsout_clicked)
        btn_search_velpsout = QtGui.QPushButton()
        btn_search_velpsout.setText('...')
        btn_search_velpsout.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_velpsout.clicked.connect(self.btn_search_velpsout_clicked)

        # -> settings to layout
        layout_veloutput_data.addRow(self.line_velpout, btn_search_velpout)
        layout_veloutput_data.addRow(self.line_velsout, btn_search_velsout)
        layout_veloutput_data.addRow(self.line_velpsout, btn_search_velpsout)
        group_veloutput_data.setLayout(layout_veloutput_data)
        velinout_layout.addWidget(group_veloutput_data)

        # build of button execute and cancel
        btn_settings_ok = QtGui.QPushButton()
        btn_settings_ok.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        btn_settings_ok.setText('Execute!')
        btn_settings_ok.clicked.connect(self.btn_relocate_ok_clicked)

        btn_settings_test = QtGui.QPushButton()
        btn_settings_test.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_settings_test.setText('Test Resolution!')
        btn_settings_test.clicked.connect(self.btn_relocate_test_clicked)

        # -> settings to layout
        okcancel_layout = QtGui.QHBoxLayout()
        okcancel_layout.addWidget(btn_settings_ok)
        okcancel_layout.addWidget(btn_settings_test)
        layout_parameters.addRow(okcancel_layout)

    def execute_this_btn_relocate_test_clicked(self, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()
        if self.type.currentIndex() == 0:
            x, y, z, vxyz, velr, rms = inversion_test(self.line_evtdat.text(), self.line_statdat.text(),
                                                      self.line_veldat.text(), float(self.deg2km.text()),
                                                      int(self.nx.text()),
                                                      int(self.ny.text()), int(self.nz.text()),
                                                      float(self.normd.text()), float(self.gradd.text()),
                                                      int(self.iter.text()),
                                                      int(self.split.text()), int(self.biter.text()),
                                                      int(self.cacah.text()), float(self.pert.text()),progress_callback)
            np.ndarray.tofile(vxyz, self.line_velcalout.text())
            np.ndarray.tofile(velr, self.line_velobsout.text())
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(), self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(), self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(), self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS:' + '\n')
            for i in range(len(rms)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rms[i]) + '\n')
            file.close()

        if self.type.currentIndex() == 1:
            x, y, z, vxyz, velr, rms = inversion_testS(self.line_evtdat.text(), self.line_statdat.text(),
                                                       self.line_veldat.text(), float(self.deg2km.text()),
                                                       int(self.nx.text()),
                                                       int(self.ny.text()), int(self.nz.text()),
                                                       float(self.normd.text()), float(self.gradd.text()),
                                                       int(self.iter.text()),
                                                       int(self.split.text()), int(self.biter.text()),
                                                       int(self.cacah.text()), float(self.pert.text()),progress_callback)
            np.ndarray.tofile(vxyz, self.line_velcalout.text())
            np.ndarray.tofile(velr, self.line_velobsout.text())
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(),
                     self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(),
                     self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(),
                     self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS:' + '\n')
            for i in range(len(rms)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rms[i]) + '\n')
            file.close()

        if self.type.currentIndex() == 2:
            x, y, z, vxyzp, velrp, rmsp = inversion_test(self.line_evtdat.text(), self.line_statdat.text(),
                                                         self.line_veldat.text(), float(self.deg2km.text()),
                                                         int(self.nx.text()),
                                                         int(self.ny.text()), int(self.nz.text()),
                                                         float(self.normd.text()), float(self.gradd.text()),
                                                         int(self.iter.text()),
                                                         int(self.split.text()), int(self.biter.text()),
                                                         int(self.cacah.text()), float(self.pert.text()),progress_callback)
            x, y, z, vxyzs, velrs, rmss = inversion_testS(self.line_evtdat.text(), self.line_statdat.text(),
                                                          self.line_veldat.text(), float(self.deg2km.text()),
                                                          int(self.nx.text()),
                                                          int(self.ny.text()), int(self.nz.text()),
                                                          float(self.normd.text()), float(self.gradd.text()),
                                                          int(self.iter.text()),
                                                          int(self.split.text()), int(self.biter.text()),
                                                          int(self.cacah.text()), float(self.pert.text()),progress_callback)
            vxyzps = vxyzp / vxyzs
            velrps = velrp / velrs
            pathcal = self.line_velcalout.text().split('.')
            pathobs = self.line_velobsout.text().split('.')
            np.ndarray.tofile(vxyzp, pathcal[0] + '-P.' + pathcal[1])
            np.ndarray.tofile(velrp, pathobs[0] + '-P.' + pathobs[1])
            np.ndarray.tofile(vxyzs, pathcal[0] + '-S.' + pathcal[1])
            np.ndarray.tofile(velrs, pathobs[0] + '-S.' + pathobs[1])
            np.ndarray.tofile(vxyzps, pathcal[0] + '-PS.' + pathcal[1])
            np.ndarray.tofile(velrps, pathobs[0] + '-PS.' + pathobs[1])
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(),
                     self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(),
                     self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(),
                     self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS P:' + '\n')
            for i in range(len(rmsp)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rmsp[i]) + '\n')
            file.write('\n' + 'RMS S:' + '\n')
            for i in range(len(rmss)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rmss[i]) + '\n')
            file.close()
        elt = tac()
        return elt

    def btn_relocate_test_clicked_output(self, s):
        file = open(self.line_velog.text(), 'a')
        file.write('Elapsed Time:' + '\t' + s + '\n')

    def btn_relocate_test_clicked_complete(self):
        self.labstat.setText('Status: Finished')

    def progress_btn_relocate_test_clicked(self, n):
        self.labstat.setText(n)

    def btn_relocate_test_clicked_error(self):
        self.message = MessageBox()
        self.message.show()

    def btn_relocate_test_clicked(self):
        # Pass the function to execute
        worker = Worker(
            self.execute_this_btn_relocate_test_clicked)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.btn_relocate_test_clicked_output)
        worker.signals.error.connect(self.btn_relocate_test_clicked_error)
        worker.signals.finished.connect(self.btn_relocate_test_clicked_complete)
        worker.signals.progress.connect(self.progress_btn_relocate_test_clicked)

        # Execute
        self.threadpool.start(worker)

    def execute_this_btn_relocate_ok_clicked(self, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()
        if self.type.currentIndex() == 0:
            x, y, z, vxyz, rms = inversion(self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                                           float(self.deg2km.text()), int(self.nx.text()),
                                           int(self.ny.text()), int(self.nz.text()), float(self.normd.text()),
                                           float(self.gradd.text()), int(self.iter.text()),
                                           int(self.split.text()), int(self.biter.text()), int(self.cacah.text()),
                                           progress_callback)
            np.ndarray.tofile(vxyz, self.line_velpout.text())
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(),
                     self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(),
                     self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(),
                     self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS:' + '\n')
            for i in range(len(rms)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rms[i]) + '\n')
            file.close()

        if self.type.currentIndex() == 1:
            x, y, z, vxyz, rms = inversionS(self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                                            float(self.deg2km.text()), int(self.nx.text()),
                                            int(self.ny.text()), int(self.nz.text()), float(self.normd.text()),
                                            float(self.gradd.text()), int(self.iter.text()),
                                            int(self.split.text()), int(self.biter.text()), int(self.cacah.text()),
                                            progress_callback)
            np.ndarray.tofile(vxyz, self.line_velsout.text())
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(),
                     self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(),
                     self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(),
                     self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS:' + '\n')
            for i in range(len(rms)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rms[i]) + '\n')
            file.close()

        if self.type.currentIndex() == 2:
            x, y, z, vxyzp, rmsp = inversion(self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                                             float(self.deg2km.text()), int(self.nx.text()),
                                             int(self.ny.text()), int(self.nz.text()), float(self.normd.text()),
                                             float(self.gradd.text()), int(self.iter.text()),
                                             int(self.split.text()), int(self.biter.text()), int(self.cacah.text()),
                                             progress_callback)
            x, y, z, vxyzs, rmss = inversionS(self.line_evtdat.text(), self.line_statdat.text(),
                                              self.line_veldat.text(),
                                              float(self.deg2km.text()), int(self.nx.text()),
                                              int(self.ny.text()), int(self.nz.text()), float(self.normd.text()),
                                              float(self.gradd.text()), int(self.iter.text()),
                                              int(self.split.text()), int(self.biter.text()), int(self.cacah.text()),
                                              progress_callback)
            vxyzps = vxyzp / vxyzs
            np.ndarray.tofile(vxyzp, self.line_velpout.text())
            np.ndarray.tofile(vxyzs, self.line_velsout.text())
            np.ndarray.tofile(vxyzps, self.line_velpsout.text())
            np.ndarray.tofile(x, self.line_xout.text())
            np.ndarray.tofile(y, self.line_yout.text())
            np.ndarray.tofile(z, self.line_zout.text())
            tomo_log(self.line_velog.text(), self.line_evtdat.text(), self.line_statdat.text(), self.line_veldat.text(),
                     self.line_xout.text(), self.line_yout.text(), self.line_zout.text(), self.line_velog.text(),
                     self.line_velobsout.text(), self.line_velcalout.text(), self.line_velpout.text(),
                     self.line_velsout.text(),
                     self.line_velpsout.text(), self.type.currentText(), self.deg2km.text(), self.nx.text(),
                     self.ny.text(),
                     self.nz.text(), self.normd.text(), self.gradd.text(), self.iter.text(), self.cacah.text(),
                     self.biter.text(),
                     self.split.text(), self.pert.text())
            file = open(self.line_velog.text(), 'a')
            file.write('\n' + 'RMS P:' + '\n')
            for i in range(len(rmsp)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rmsp[i]) + '\n')
            file.write('\n' + 'RMS S:' + '\n')
            for i in range(len(rmss)):
                file.write('Iteration' + '\t' + str(i + 1) + ':' + '\t')
                file.write(str(rmss[i]) + '\n')
            file.close()
        elt = tac()
        return elt

    def btn_relocate_ok_clicked_output(self, s):
        file = open(self.line_velog.text(), 'a')
        file.write('Elapsed Time:' + '\t' + s + '\n')

    def btn_relocate_ok_clicked_complete(self):
        self.labstat.setText('Status: Finished')

    def progress_btn_relocate_ok_clicked(self, n):
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

    def btn_search_evtdat_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open event (*.evt) file', '/', "Format File (*.evt)")
        self.line_evtdat.setText(filepath[0])

    def btn_search_statdat_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station (*.dat) file', '/', "Format File (*.dat)")
        self.line_statdat.setText(filepath[0])

    def btn_search_veldat_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velocity (*.vel) file', '/', "Format File (*.vel)")
        self.line_veldat.setText(filepath[0])

    def btn_search_velout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velout.setText(filepath[0])

    def btn_search_velobsout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save obs velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velobsout.setText(filepath[0])

    def btn_search_velcalout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save cal velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velcalout.setText(filepath[0])

    def btn_search_velpout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save P velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velpout.setText(filepath[0])

    def btn_search_velsout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save S velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velsout.setText(filepath[0])

    def btn_search_velpsout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save P/S velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_velpsout.setText(filepath[0])

    def btn_search_xout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save x (*.data) file', '/', "Format File (*.data)")
        self.line_xout.setText(filepath[0])

    def btn_search_yout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save y (*.data) file', '/', "Format File (*.data)")
        self.line_yout.setText(filepath[0])

    def btn_search_zout_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save z (*.data) file', '/', "Format File (*.data)")
        self.line_zout.setText(filepath[0])

    def btn_search_velog_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getSaveFileName(self, 'Save log (*.log) file', '/', "Format File (*.log)")
        self.line_velog.setText(filepath[0])

    def act_enter_nset(self):
        self.table_weighting.setRowCount(int(self.nset.text()))

    def closeTab_tabel (self, currentIndex):
        currentQWidget = self.tab_tabel.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tab_tabel.removeTab(currentIndex)

    def tab_data(self):
        self.main_data = QtGui.QWidget()
        self.data_layout = QtGui.QVBoxLayout()
        self.tab_tabel = QtGui.QTabWidget()
        self.tab_tabel.setTabsClosable(True)
        self.tab_tabel.tabCloseRequested.connect(self.closeTab_tabel)

        # path
        # -> build upper layout
        path_layout = QtGui.QHBoxLayout()

        # -> filled
        self.line_data = QtGui.QLineEdit()
        self.line_data.setPlaceholderText('path of data (all file format)')
        btn_search_data = QtGui.QPushButton()
        btn_search_data.setText('...')
        btn_search_data.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_data.clicked.connect(self.btn_search_data_clicked)

        btn_enter_data = QtGui.QPushButton()
        btn_enter_data.setText('View!')
        btn_enter_data.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
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
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open file', '/', "Format File (*.*)")
        self.line_data.setText(filepath[0])

    def btn_enter_data_clicked(self):
        graph_widget = QtGui.QWidget()
        graph_layout = QtGui.QVBoxLayout()
        file = open(self.line_data.text(), 'r')
        viewit = file.read()

        # view
        tabel = QtGui.QTextEdit()
        tabel.setText(viewit)

        graph_layout.addWidget(tabel)
        graph_widget.setLayout(graph_layout)
        self.tab_tabel.addTab(graph_widget,self.line_data.text().split('/')[-1])

    def closeTab (self, currentIndex):
        currentQWidget = self.tab_graph.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tab_graph.removeTab(currentIndex)

    def tab_view2D(self):
        self.main_view2D = QtGui.QWidget()
        self.view_layout = QtGui.QVBoxLayout()
        self.tab_graph = QtGui.QTabWidget()
        self.tab_graph.setTabsClosable(True)
        self.tab_graph.tabCloseRequested.connect(self.closeTab)

        # path
        # -> build upper layout
        path_layout = QtGui.QHBoxLayout()

        # -> filled
        self.line_vxyz = QtGui.QLineEdit()
        self.line_vxyz.setPlaceholderText('path of vel3d (*.vel3d)')
        btn_search_vxyz = QtGui.QToolButton()
        btn_search_vxyz.setText('...')
        btn_search_vxyz.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        btn_search_vxyz.clicked.connect(self.btn_search_vxyz_clicked)

        self.line_xdata = QtGui.QLineEdit()
        self.line_xdata.setPlaceholderText('path of xdata (*.data)')
        btn_search_xdata = QtGui.QToolButton()
        btn_search_xdata.setText('...')
        btn_search_xdata.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_xdata.clicked.connect(self.btn_search_xdata_clicked)

        self.line_ydata = QtGui.QLineEdit()
        self.line_ydata.setPlaceholderText('path of ydata (*.data)')
        btn_search_ydata = QtGui.QToolButton()
        btn_search_ydata.setText('...')
        btn_search_ydata.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_ydata.clicked.connect(self.btn_search_ydata_clicked)

        self.line_zdata = QtGui.QLineEdit()
        self.line_zdata.setPlaceholderText('path of zdata (*.data)')
        btn_search_zdata = QtGui.QToolButton()
        btn_search_zdata.setText('...')
        btn_search_zdata.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_zdata.clicked.connect(self.btn_search_zdata_clicked)

        self.line_log = QtGui.QLineEdit()
        self.line_log.setPlaceholderText('path of log (*.log)')
        btn_search_log = QtGui.QToolButton()
        btn_search_log.setText('...')
        btn_search_log.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_search_log.clicked.connect(self.btn_search_log_clicked)

        btn_enter_view = QtGui.QPushButton()
        btn_enter_view.setText('View!')
        btn_enter_view.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_enter_view.clicked.connect(self.btn_enter_view_clicked)

        # -> input to layout
        path_layout.addWidget(self.line_vxyz)
        path_layout.addWidget(btn_search_vxyz)
        path_layout.addWidget(self.line_xdata)
        path_layout.addWidget(btn_search_xdata)
        path_layout.addWidget(self.line_ydata)
        path_layout.addWidget(btn_search_ydata)
        path_layout.addWidget(self.line_zdata)
        path_layout.addWidget(btn_search_zdata)
        path_layout.addWidget(self.line_log)
        path_layout.addWidget(btn_search_log)
        path_layout.addWidget(btn_enter_view)
        self.view_layout.addLayout(path_layout)
        self.view_layout.addWidget(self.tab_graph)

        # input layout to widget
        self.main_view2D.setLayout(self.view_layout)

    def btn_search_vxyz_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velocity 3D (*.vel3d) file', '/', "Format File (*.vel3d)")
        self.line_vxyz.setText(filepath[0])

    def btn_search_xdata_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open x (*.data) file', '/', "Format File (*.data)")
        self.line_xdata.setText(filepath[0])

    def btn_search_ydata_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open y (*.data) file', '/', "Format File (*.data)")
        self.line_ydata.setText(filepath[0])

    def btn_search_zdata_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open z (*.data) file', '/', "Format File (*.data)")
        self.line_zdata.setText(filepath[0])

    def btn_search_log_clicked(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open log (*.log) file', '/', "Format File (*.log)")
        self.line_log.setText(filepath[0])

    # create menubar
    def menubar(self):
        self.mbar = self.menuBar()
        self.file = self.mbar.addMenu('File')
        self.reopen = self.file.addAction('Extract Info from Log File')
        self.convert = self.mbar.addMenu('Convert')
        self.dd2tomo = self.convert.addAction('hypoDD to Tomo File')
        self.process = self.mbar.addMenu('Analysis')
        self.analyze2d = self.process.addAction('2D Analyze')
        self.analyze3d = self.process.addAction('3D Analyze')
        self.welltomo = self.process.addAction('Cross Well Tomography')
        self.error23d = self.process.addAction('Create 2D/3D Error')
        self.viewRay = self.process.addAction('Ray Tracing View')
        self.help = self.mbar.addAction('Help')

        # add signal and slot to menubar
        self.dd2tomo.triggered.connect(self.act_dd2tomo)
        self.reopen.triggered.connect(self.act_reopen)
        self.analyze2d.triggered.connect(self.act_analyze2d)

        # disabled
        self.file.setDisabled(True)
        self.convert.setDisabled(True)
        self.process.setDisabled(True)
        self.help.setDisabled(True)

    # action of bmkg2pha
    def act_dd2tomo(self):
        # build form ph2dt
        self.form_bmkg2pha = QtGui.QWidget()
        mainwidget = QtGui.QWidget(self.form_bmkg2pha)
        # self.form_bmkg2pha.setWindowTitle('Wizard hypoDD to Tomo File')
        # self.form_bmkg2pha.setWindowFlag(QtGui.Qt.WindowStaysOnTopHint)

        # build main layout
        mainlayout = QtGui.QVBoxLayout()

        # build group of input data
        group_input_data = QtGui.QGroupBox()
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QtGui.QFormLayout()

        # -> filled
        self.line_reloc = QtGui.QLineEdit()
        self.line_reloc.setPlaceholderText('Path for hypoDD.reloc (*.reloc')
        self.line_phase = QtGui.QLineEdit()
        self.line_phase.setPlaceholderText('Path for hypoDD.pha (*.pha')

        btn_search_reloc = QtGui.QPushButton()
        btn_search_reloc.setText('...')
        btn_search_reloc.clicked.connect(self.btn_search_reloc_clicked)
        btn_search_phase = QtGui.QPushButton()
        btn_search_phase.setText('...')
        btn_search_phase.clicked.connect(self.btn_search_phase_clicked)


        # -> settings to layout
        layout_input_data.addRow(self.line_reloc, btn_search_reloc)
        layout_input_data.addRow(self.line_phase, btn_search_phase)
        group_input_data.setLayout(layout_input_data)
        mainlayout.addWidget(group_input_data)

        # build group of output data
        group_output_data = QtGui.QGroupBox()
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QtGui.QFormLayout()

        # -> filled
        self.line_event = QtGui.QLineEdit()
        self.line_event.setPlaceholderText('Path for tomo_event.evt (*.evt)')

        btn_search_event = QtGui.QPushButton()
        btn_search_event.setText('...')
        btn_search_event.clicked.connect(self.btn_search_event_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_event, btn_search_event)
        group_output_data.setLayout(layout_output_data)
        mainlayout.addWidget(group_output_data)

        # build of button execute and cancel
        btn_settings_ok = QtGui.QPushButton()
        btn_settings_ok.setText('OK')
        btn_settings_ok.clicked.connect(self.btn_bmkg2pha_ok_clicked)
        btn_settings_cancel = QtGui.QPushButton()
        btn_settings_cancel.setText('Cancel')
        btn_settings_cancel.clicked.connect(self.btn_bmkg2pha_cancel_clicked)

        # -> settings to layout
        okcancel_layout = QtGui.QHBoxLayout()
        okcancel_layout.addWidget(btn_settings_ok)
        okcancel_layout.addWidget(btn_settings_cancel)
        mainlayout.addLayout(okcancel_layout)

        # setting layouts to form
        mainwidget.setLayout(mainlayout)
        mainwidget.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        mainlay = QtGui.QHBoxLayout()
        mainlay.addWidget(mainwidget)
        self.form_bmkg2pha.setLayout(mainlay)

        # show form bmkg2pha
        self.form_bmkg2pha.show()
        # self.maintab.addTab(self.form_bmkg2pha, self.icon_tab_tg, 'hypoDD to Tomo File')
        # self.form_bmkg2pha.show()

    # back end of bmkg2pha
    def btn_search_reloc_clicked(self):
        open = QtGui.QFileDialog()
        bmkg_filepath = open.getOpenFileName(self, 'Open hypoDD.reloc file', '/',"Format File (*.reloc)")
        self.line_reloc.setText(bmkg_filepath[0])

    def btn_search_phase_clicked(self):
        open = QtGui.QFileDialog()
        bmkg_filepath = open.getOpenFileName(self, 'Open hypoDD.pha file', '/',"Format File (*.pha)")
        self.line_phase.setText(bmkg_filepath[0])

    def btn_search_event_clicked(self):
        save = QtGui.QFileDialog()
        pha_filepath = save.getSaveFileName(self, 'Save tomo event file', '/',"Format File (*.evt)")
        self.line_event.setText(pha_filepath[0])

    def act_reopen(self):
        open = QtGui.QFileDialog()
        filepath = open.getOpenFileName(self, 'Open .log file', '/', "Format File (*.log)")

        if filepath[0] != '':
            evtdat, statdat, veldat, xout, yout, zout, velog, velobsout, velcalout, velpout, velsout, velpsout, type, \
            deg2km, nx, ny, nz, normd, gradd, iter, cacah, biter, split, pert = read_log(filepath[0])
            self.line_evtdat.setText(evtdat)
            self.line_statdat.setText(statdat)
            self.line_veldat.setText(veldat)
            self.line_xout.setText(xout)
            self.line_yout.setText(yout)
            self.line_zout.setText(zout)
            self.line_velog.setText(velog)
            self.line_velobsout.setText(velobsout)
            self.line_velcalout.setText(velcalout)
            self.line_velpout.setText(velpout)
            self.line_velsout.setText(velsout)
            self.line_velpsout.setText(velpsout)
            self.type.setCurrentText(type)
            self.deg2km.setText(deg2km)
            self.nx.setText(nx)
            self.ny.setText(ny)
            self.nz.setText(nz)
            self.normd.setText(normd)
            self.gradd.setText(gradd)
            self.iter.setText(iter)
            self.cacah.setText(cacah)
            self.biter.setText(biter)
            self.split.setText(split)
            self.pert.setText(pert)

    def act_analyze2d(self):
        icon_tab_tg = QtGui.QIcon()
        icon_tab_tg.addPixmap(QtGui.QPixmap(icon_tomo), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # tab_analyze2d = an2d.MainWindow()
        # tab_analyze2d.show()
        # self.maintab.addTab(tab_analyze2d, icon_tab_tg, "2D Analyze")

    def btn_bmkg2pha_ok_clicked(self):
        ht.dd2tomo(self.line_reloc.text(), self.line_phase.text(), self.line_event.text())
        self.form_bmkg2pha.close()

    def btn_bmkg2pha_cancel_clicked(self):
        self.form_bmkg2pha.close()

# execute by system
if __name__ == '__main__':
    App = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(App.exec_())