import sys
from pyface.qt import QtGui, QtCore
import os

def bmkg2pha(fileinput, fileoutput):
    # membaca data dari file input dan memulai membuat file output
    file = open(fileinput, 'r')
    baris = file.readlines()
    for i in range(len(baris)):
        baris[i] = baris[i].split()
    file.close()
    file = open(fileoutput, 'w')

    # menyalin data tiap baris file input ke dalam file output
    i = 0
    event = 0
    while i < len(baris):
        if len(baris[i]) > 0 and baris[i][0] == 'EventID:':
            event = event + 1
            eventid = baris[i][1][3::]
            tahun = baris[i + 2][0].split('-')[0]
            bulan = baris[i + 2][0].split('-')[1].zfill(2)
            tanggal = baris[i + 2][0].split('-')[2].zfill(2)
            jam = baris[i + 2][1].split(':')[0].zfill(2)
            menit = baris[i + 2][1].split(':')[1].zfill(2)
            detik = (('%.1f') % float(baris[i + 2][1].split(':')[0])).zfill(4)
            lintang = (('%.2f') % float(baris[i + 2][2])).zfill(6)
            bujur = (('%.2f') % float(baris[i + 2][3])).zfill(6)
            depth = ('%.1f') % float(baris[i + 2][4])
            mag = ('%.1f') % float(baris[i + 2][5])
            unknown = '0.0'
            rms = ('%.3f') % float(baris[i + 2][10])
            time0 = float(detik) + float(menit) * 60 + float(jam) * 3600 + float(tanggal) * 24 * 3600
            file.write('#' + '\t' + tahun
                       + '\t' + bulan
                       + '\t' + tanggal
                       + '\t' + jam
                       + '\t' + menit
                       + '\t' + detik
                       + '\t' + lintang
                       + '\t' + bujur
                       + '\t' + depth
                       + '\t' + mag
                       + '\t' + unknown
                       + '\t' + unknown
                       + '\t' + rms
                       + '\t' + str(event)
                       + '\n')
        if len(baris[i]) > 0 and baris[i][0] == 'Net':
            try:
                j = 0
                while j < 1:
                    i = i + 1
                    try:
                        idSta = baris[i][1]
                        phase = baris[i][2]
                        tanggal = baris[i][3].split('-')[2]
                        jam = baris[i][4].split(':')[0]
                        menit = baris[i][4].split(':')[1]
                        detik = baris[i][4].split(':')[2]
                        time1 = float(detik) + float(menit) * 60 + float(jam) * 3600 + float(tanggal) * 24 * 3600
                        deltatime = ('%.2f') % float(time1 - time0)
                        unknown = '1.000'
                        file.write(idSta.rjust(5)
                                   + deltatime.rjust(12)
                                   + unknown.rjust(8)
                                   + phase.rjust(4)
                                   + '\n'
                                   )
                    except:
                        break
            except:
                break
        i = i + 1
    file.close()

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        mainwidget = QtGui.QWidget(self)
        self.setWindowTitle('Wizard BMKG buletin to PHA')
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # build main layout
        mainlayout = QtGui.QVBoxLayout()

        # build group of input data
        group_input_data = QtGui.QGroupBox()
        group_input_data.setTitle('Path of Input Data')
        layout_input_data = QtGui.QFormLayout()

        # -> filled
        self.line_BMKG = QtGui.QLineEdit()
        self.line_BMKG.setPlaceholderText('Path for BMKG buletin (*.*')

        btn_search_BMKG = QtGui.QPushButton()
        btn_search_BMKG.setText('...')
        btn_search_BMKG.clicked.connect(self.btn_search_BMKG_clicked)

        # -> settings to layout
        layout_input_data.addRow(self.line_BMKG, btn_search_BMKG)
        group_input_data.setLayout(layout_input_data)
        mainlayout.addWidget(group_input_data)

        # build group of output data
        group_output_data = QtGui.QGroupBox()
        group_output_data.setTitle('Path of Output Data')
        layout_output_data = QtGui.QFormLayout()

        # -> filled
        self.line_pha = QtGui.QLineEdit()
        self.line_pha.setPlaceholderText('Path for output .pha')

        btn_search_pha = QtGui.QPushButton()
        btn_search_pha.setText('...')
        btn_search_pha.clicked.connect(self.btn_search_pha_clicked)

        # -> settings to layout
        layout_output_data.addRow(self.line_pha, btn_search_pha)
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
        self.setCentralWidget(mainwidget)

        # show form bmkg2pha
        self.show()

    def btn_search_BMKG_clicked(self):
        open = QtGui.QFileDialog()
        bmkg_filepath = open.getOpenFileName(self, 'Open BMKG file', '/',"Format File (*.*)")
        self.line_BMKG.setText(bmkg_filepath[0])

    def btn_search_pha_clicked(self):
        save = QtGui.QFileDialog()
        pha_filepath = save.getSaveFileName(self, 'Save PHA file', '/',"Format File (*.pha)")
        self.line_pha.setText(pha_filepath[0])

    def btn_bmkg2pha_ok_clicked(self):
        if self.line_BMKG.text() != "" and self.line_pha.text() != "":
            bmkg2pha(self.line_BMKG.text(),self.line_pha.text())
        self.close()

    def btn_bmkg2pha_cancel_clicked(self):
        self.close()