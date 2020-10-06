import sys
from pyface.qt.QtGui import QFileDialog, QTableWidgetItem
from obspy import read


def Open(window):
    # Open the data
    opendialog = QFileDialog()
    filename = opendialog.getOpenFileName(window, 'Open Seismogram File', '/', "Format File (*.mseed *.SAC)")
    file_data = read(filename)
    return filename, file_data


def inputtable(data, database_index, tbl_info):
    for i in range(int(data.count())):
        idx = i
        database_index.append(idx)
        tr_data =data.pop(0)
        input_to_informationtable(tbl_info, tr_data)

def input_to_informationtable(tbl_info, tr_data):
    n = tbl_info.rowCount()
    tbl_info.insertRow(n)

    # Set table
    tbl_info.setItem(n - 1, 0, QTableWidgetItem(str(tr_data.stats.network)))
    tbl_info.setItem(n - 1, 1, QTableWidgetItem(str(tr_data.stats.station)))
    tbl_info.setItem(n - 1, 2, QTableWidgetItem(str(tr_data.stats.location)))
    tbl_info.setItem(n - 1, 3, QTableWidgetItem(str(tr_data.stats.channel)))
    tbl_info.setItem(n - 1, 4, QTableWidgetItem(str(tr_data.stats.starttime)))
    tbl_info.setItem(n - 1, 5, QTableWidgetItem(str(tr_data.stats.endtime)))
    tbl_info.setItem(n - 1, 6, QTableWidgetItem(str(tr_data.stats.sampling_rate)))
    tbl_info.setItem(n - 1, 7, QTableWidgetItem(str(tr_data.stats.delta)))
    tbl_info.setItem(n - 1, 8, QTableWidgetItem(str(tr_data.stats.npts)))
    tbl_info.setItem(n - 1, 9, QTableWidgetItem(str(tr_data.stats.calib)))
    tbl_info.setItem(n - 1, 10, QTableWidgetItem(str(tr_data.stats._format)))
