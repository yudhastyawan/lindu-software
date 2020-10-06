import sys
from pyface.qt.QtCore import *
from pyface.qt.QtGui import *
import os

from plugins.seismolist.modules.Action import *

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Seismo List')
        self.icon = QIcon(os.path.join(os.getcwd(),'subroutine','icon','Icon_Files','FIX','LOGO.ico'))
        self.setWindowIcon(self.icon)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.showMaximized()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tbl_info = QTableWidget()
        self.setTable()

        # Data Loop
        self.count = 0
        self.database_index = []
        self.database_filename= []


        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QGroupBox()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Getting Started")

        self.tabs.addTab(self.tab2, "Datasets")
        self.tabs.setTabEnabled(1, False)

        # Create 1st
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QCommandLinkButton("Load Data")
        self.pushButton1.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.pushButton1.clicked.connect(self.loadData)
        lbl_getting = QLabel()

        lbl2_getting = QLabel()
        # lbl_getting.setScaledContents(True)
        # lbl_getting.setMaximumSize(getting_pixmap.width(),getting_pixmap.height())
        lbl_getting.setAlignment(Qt.AlignHCenter)
        lbl_getting.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        lbl2_getting.setAlignment(Qt.AlignHCenter)
        lbl2_getting.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.tab1.layout.addSpacing(150)
        self.tab1.layout.addWidget(lbl_getting)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.layout.addWidget(lbl2_getting)
        self.tab1.layout.addSpacing(300)
        self.tab1.layout.setAlignment(self.pushButton1, Qt.AlignTop|Qt.AlignHCenter)


        # self.tab1.layout.setAlignment(self.pushButton1, Qt.AlignHCenter)
        self.tab1.setLayout(self.tab1.layout)


        # Create 2nd tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.tbl_info)
        self.tab2.setLayout(self.tab2.layout)

        # Create 3rd tab
        self.createHorizontalLayout()
        self.createHH()
        self.tab3.layout = QHBoxLayout()
        self.tab3.layout.addWidget(self.horizontalGroupBox)
        self.tab3.layout.addWidget(self.HHGroupBox)
        self.tab3.setLayout(self.tab3.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        # self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("First Break Picked tools")

        # Define var for tab add req
        self.tabs_add = QTabWidget()
        self.tabs_add.setTabsClosable(True)
        self.tabs_add.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabs_add.tabCloseRequested.connect(self.closeTab)

        self.pickTitle = QLabel("Select this one to start pick time arrival")
        self.get_guide = QPushButton("Get Guide")
        self.pickP = QPushButton("Pick P")
        self.pickS = QPushButton("Pick S")
        self.export_pick = QPushButton("Export Data")

        self.b = QTableWidget()
        self.b.setRowCount(1)
        self.b.setColumnCount(5)
        self.b.setHorizontalHeaderLabels(["Station", "Channel", "Date", "Time P", "Time S"])
        self.b.setAlternatingRowColors(True)
        self.b.setEditTriggers(QTableWidget.AllEditTriggers)
        self.b.setSelectionBehavior(QTableWidget.SelectItems)
        self.b.setSelectionMode(QTableWidget.SingleSelection)


        # a.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # a.setFixedSize(350, 100)

        self.b.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.b.setFixedWidth(350)

        layout = QVBoxLayout()
        # layout.addWidget(a)
        layout.addWidget(self.pickTitle)
        layout.addWidget(self.get_guide)
        layout.addWidget(self.pickP)
        layout.addWidget(self.pickS)
        layout.addWidget(self.b)
        layout.addWidget(self.export_pick)

        self.horizontalGroupBox.setLayout(layout)

    def createHH(self):
        self.HHGroupBox = QGroupBox("Data Visualization")
        a = QTableWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.tabs_add)
        self.HHGroupBox.setLayout(layout)

    def loadData(self):
        self.open_file, file_data = Open(self)
        # print(file_data[0])

        file = open('filename.user','a')

        for i in range(int(file_data.count())):
            self.idx = i
            self.database_index.append(self.idx)
            file.write(
                self.open_file[0]+'\n'
            )
            # self.database_filename.append(self.open_file[0])
            self.tr_data = file_data.pop(0)
            input_to_informationtable(self.tbl_info, self.tr_data )
        file.close()

        # Off tabs feature
        self.tabs.setTabEnabled(1, True)
        self.tabs.setCurrentIndex(1)


    def setTable(self):
        self.tbl_info.clear()
        self.tbl_info.setRowCount(1)
        self.tbl_info.setColumnCount(11)
        self.tbl_info.setHorizontalHeaderLabels(
            ["Network", "Station", "Location", "Channel", "Start Time",
             "End Time", "Sampling Rate", "Delta", "NPTS", "Calib", "Format"])
        self.tbl_info.setAlternatingRowColors(True)
        self.tbl_info.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl_info.setSelectionBehavior(QTableWidget.SelectRows)
        self.tbl_info.setSelectionMode(QTableWidget.MultiSelection)
        selected = None

    def pick_table(self):
        self.pick_info.clear()
        self.pick_info.setRowCount(1)
        self.pick_info.setColumnCount(5)
        # self.pick_info.

    def contextMenuEvent(self, event):
        self.menu = QMenu(self.tbl_info)
        self.plot_menu = self.menu.addAction("Plot")
        self.plot_menu.triggered.connect(self.index_selected)
        self.menu.exec_(event.globalPos())


    def index_selected(self):
        print("\n")
        self.idx = []
        i = 0
        for currentQTableWidgetItem in self.tbl_info.selectedItems():
            if len(self.idx) == 0:
                i = i + 1
                self.idx.append(currentQTableWidgetItem.row())
            elif len(self.idx) != 0 and self.idx[i - 1] != currentQTableWidgetItem.row():
                i = i + 1
                self.idx.append(currentQTableWidgetItem.row())

            # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

        print(self.idx)
        print(i)
        self.tabs.setTabEnabled(2, True)
        self.tabs.setCurrentIndex(2)

    def onpick(self, event):
        thisline = event.artist

        self.xdata = thisline.get_xdata()
        ind = event.ind[0]
        time = mpl.dates.num2date(self.xdata[ind])

        self.date_pick = str(time).split()[0]
        self.time_pick = str(time).split()[1].split("+")[0]
        self.hour_pick = str(time).split()[1].split("+")[0].split(":")[0]
        self.minute_pick = str(time).split()[1].split("+")[0].split(":")[1]
        self.second_pick = str(time).split()[1].split("+")[0].split(":")[2]

        ydata = thisline.get_ydata()
        # ind = event.ind
        points = (self.xdata[ind], ydata[ind])
        print('onpick points:', points, time)
        line, = self.ax1.plot(self.xdata[ind], 0, 'r|', MarkerSize = 1000)

        # Calling table input
        self.input_to_pickP(self.b, self.data_plot, self.date_pick, self.time_pick)
        self.fig.canvas.mpl_disconnect(self.a)

    def plot_pickP(self):
        self.a = self.fig.canvas.mpl_connect('pick_event', self.onpick)

    def onpickS(self, event):
        thisline = event.artist

        self.xdata = thisline.get_xdata()
        ind = event.ind[0]
        time = mpl.dates.num2date(self.xdata[ind])

        self.date_pick = str(time).split()[0]
        self.time_pick = str(time).split()[1].split("+")[0]
        self.hour_pick = str(time).split()[1].split("+")[0].split(":")[0]
        self.minute_pick = str(time).split()[1].split("+")[0].split(":")[1]
        self.second_pick = str(time).split()[1].split("+")[0].split(":")[2]

        ydata = thisline.get_ydata()
        # ind = event.ind
        points = (self.xdata[ind], ydata[ind])
        print('onpick points:', points, time)
        line, = self.ax1.plot(self.xdata[ind], 0, 'b|', MarkerSize = 1000)

        # Calling table input
        self.input_to_pickS(self.b, self.data_plot, self.date_pick, self.time_pick)
        self.fig.canvas.mpl_disconnect(self.a)

    def plot_pickS(self):
        # self.fig.canvas.mpl_disconnect()
        self.a = self.fig.canvas.mpl_connect('pick_event', self.onpickS)

    def closeTab(self, currentIndex):
        currentQWidget = self.tabs_add.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabs_add.removeTab(currentIndex)

    def input_to_pickP(self, b, data_plot, date_pick, time_pick):
        n = b.rowCount()
        b.insertRow(n)
        b.setItem(n - 1, 0, QTableWidgetItem(str(data_plot.stats.station)))
        b.setItem(n - 1, 1, QTableWidgetItem(str(data_plot.stats.channel)))
        b.setItem(n - 1, 2, QTableWidgetItem(str(date_pick)))
        b.setItem(n - 1, 3, QTableWidgetItem(str(time_pick)))
        b.setItem(n - 1, 4, QTableWidgetItem(str("-")))

    def input_to_pickS(self, b, data_plot, date_pick, time_pick):
        n = b.rowCount()
        b.insertRow(n)
        b.setItem(n - 1, 0, QTableWidgetItem(str(data_plot.stats.station)))
        b.setItem(n - 1, 1, QTableWidgetItem(str(data_plot.stats.channel)))
        b.setItem(n - 1, 2, QTableWidgetItem(str(date_pick)))
        b.setItem(n - 1, 3, QTableWidgetItem(str("-")))
        b.setItem(n - 1, 4, QTableWidgetItem(str(time_pick)))