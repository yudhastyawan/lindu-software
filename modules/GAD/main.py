import subprocess
import shutil
from lindugui import LMainWindow, \
    tic, tac, Worker, \
    MessageBox, MessageOpt, \
    os, sys

from pyface.qt.QtGui import *
from pyface.qt.QtCore import *

class MainWindow(LMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # create path user
        self.direc = os.getcwd()
        self.enginespath = os.path.join(os.path.dirname(__file__), 'engine', 'engines-gad')
        self.enginesexe = os.path.join(os.path.dirname(__file__), 'engine', 'gad.exe')
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

        # setting widget to layout
        layout_central.addWidget(group_relocate)

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
        self.cmd.setWindowIcon(self.icon)
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
        self.line_statdat.setText(filepath)

    def btn_search_veldat_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open velocity.dat file', '/', "Format File (*.dat)")
        self.line_veldat.setText(filepath)

    def btn_search_arrdat_clicked(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open arrival.dat file', '/', "Format File (*.dat)")
        self.line_arrdat.setText(filepath)

    def btn_search_resdat_clicked(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save result.dat', '/', "Format File (*.dat)")
        self.line_resdat.setText(filepath)

    # create menubar
    def menubar(self):
        self.settings = self.mbar.addAction('Settings')
        self.help = self.mbar.addAction('Help')

        self.settings.triggered.connect(self.act_settings)

        # set disabled
        self.help.setDisabled(True)

    # action of settings
    def act_settings(self):
        # open from file user
        file = open(self.enginespath, 'r')
        self.user_engine = file.readlines()
        file.close()

        self.form_settings = LMainWindow()
        self.form_settings.setWindowFlags(Qt.WindowStaysOnTopHint)
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
        self.line_hypoDD.setText(filepath)

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