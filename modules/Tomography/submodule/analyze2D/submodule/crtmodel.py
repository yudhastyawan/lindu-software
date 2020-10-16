import sys

from pyface.qt.QtGui import *
from pyface.qt.QtCore import *

import modules.Tomography.submodule.analyze2D.submodule.subroutine.actCrtModel as fwd
import modules.Tomography.submodule.analyze2D.submodule.subroutine.display as disp
import modules.Tomography.submodule.analyze2D.submodule.subroutine.displayVel as dispV

from lindugui.settings.threading import Worker, MessageBox
from lindugui.settings.tictac import tic, tac

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setMainWidget()
        self.threadpool = QThreadPool()

    def setMainWidget(self):
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        # main layout
        self.mainLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        # main groupbox
        self.mainGroupBox = QGroupBox()
        self.mainGroupBox.setTitle('Settings')
        self.mainGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMainGroupBox()
        self.mainLayout.addWidget(self.mainGroupBox)

        self.viewGroupBox = QGroupBox()
        self.viewGroupBox.setTitle('View')
        # self.mainGroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.mainLayout.addWidget(self.viewGroupBox)

        # main tab widget
        mainTabLayout = QVBoxLayout()
        self.mainTabWidget = QTabWidget()
        self.setMainTabWidget()
        mainTabLayout.addWidget(self.mainTabWidget)
        self.viewGroupBox.setLayout(mainTabLayout)

        # status bar
        self.statbar = self.statusBar()
        self.labstat = QLabel()
        self.labstat.setText('status: Nothing')
        self.statbar.addWidget(self.labstat)

    def setMainGroupBox(self):
        # main layout
        layoutMainGroupBox = QVBoxLayout()
        self.mainGroupBox.setLayout(layoutMainGroupBox)

        # build group of input data
        groupInputData = QGroupBox()
        groupInputData.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        groupInputData.setTitle('Path of Input Data')
        layoutInputData = QFormLayout()

        # -> filled
        self.lineSource = QLineEdit()
        self.lineSource.setPlaceholderText('Source (*.src) path')
        self.lineStat = QLineEdit()
        self.lineStat.setPlaceholderText('Station (*.stat) path')
        self.lineVel2d = QLineEdit()
        self.lineVel2d.setPlaceholderText('2D Velocity (*.vel2d) path')

        buttonSource = QPushButton()
        buttonSource.setText('...')
        buttonSource.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonSource.clicked.connect(self.clickButtonSource)
        buttonStat = QPushButton()
        buttonStat.setText('...')
        buttonStat.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonStat.clicked.connect(self.clickButtonStat)
        buttonVel2d = QPushButton()
        buttonVel2d.setText('...')
        buttonVel2d.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonVel2d.clicked.connect(self.clickButtonVel2d)

        # -> settings to layout
        layoutInputData.addRow(self.lineSource, buttonSource)
        layoutInputData.addRow(self.lineStat, buttonStat)
        layoutInputData.addRow(self.lineVel2d, buttonVel2d)
        groupInputData.setLayout(layoutInputData)
        layoutMainGroupBox.addWidget(groupInputData)

        # build group of output data
        groupOutputData = QGroupBox()
        groupOutputData.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        groupOutputData.setTitle('Path of Output Data')
        layoutOutputData = QFormLayout()

        # -> filled
        self.lineEvent = QLineEdit()
        self.lineEvent.setPlaceholderText('Event (*.evt) path')
        self.lineRay = QLineEdit()
        self.lineRay.setPlaceholderText('Ray (*.ray2d) path')
        self.lineVelout = QLineEdit()
        self.lineVelout.setPlaceholderText('2D Velocity Out (*.vel2d) path')
        self.lineLog = QLineEdit()
        self.lineLog.setPlaceholderText('Log (*.log) path')

        buttonEvent = QPushButton()
        buttonEvent.setText('...')
        buttonEvent.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonEvent.clicked.connect(self.clickButtonEvent)
        buttonRay = QPushButton()
        buttonRay.setText('...')
        buttonRay.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonRay.clicked.connect(self.clickButtonRay)
        buttonVelout = QPushButton()
        buttonVelout.setText('...')
        buttonVelout.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonVelout.clicked.connect(self.clickButtonVelout)
        buttonLog = QPushButton()
        buttonLog.setText('...')
        buttonLog.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonLog.clicked.connect(self.clickButtonLog)

        # -> settings to layout
        layoutOutputData.addRow(self.lineEvent, buttonEvent)
        layoutOutputData.addRow(self.lineRay, buttonRay)
        layoutOutputData.addRow(self.lineVelout, buttonVelout)
        layoutOutputData.addRow(self.lineLog, buttonLog)
        groupOutputData.setLayout(layoutOutputData)
        layoutMainGroupBox.addWidget(groupOutputData)

        # build group of parameter
        groupParameter = QGroupBox()
        groupParameter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        groupParameter.setTitle('Parameters')
        layoutParameter = QFormLayout()

        # -> filled
        lb_biter = QLabel()
        lb_biter.setText('Number of Ray Iteration')
        self.biter = QLineEdit()
        self.biter.setText('100')

        lb_cacah = QLabel()
        lb_cacah.setText('Number of Part of Ray Bending')
        self.cacah = QLineEdit()
        self.cacah.setText('20')

        lb_split = QLabel()
        lb_split.setText('Number of Splitting Ray Resolution')
        self.split = QLineEdit()
        self.split.setText('100')

        lb_pert = QLabel()
        lb_pert.setText('Value of Perturbation Test')
        # lb_pert.setToolTip('Index of cluster to be relocated (0 = all)')
        self.pert = QLineEdit()
        self.pert.setText('0.3')

        # -> settings to layout
        layoutParameter.addRow(lb_biter, self.biter)
        layoutParameter.addRow(lb_cacah, self.cacah)
        layoutParameter.addRow(lb_split, self.split)
        layoutParameter.addRow(lb_pert, self.pert)
        groupParameter.setLayout(layoutParameter)
        layoutMainGroupBox.addWidget(groupParameter)

        # button
        buttonExecute = QPushButton()
        buttonExecute.setText('Execute')
        buttonExecute.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        buttonExecute.clicked.connect(self.clickButtonExecute)

        # -> settings to layout
        layoutMainGroupBox.addWidget(buttonExecute)

    def executeClickButtonExecute(self, progress_callback):
        self.labstat.setText('Status: Processing . . .')
        tic()
        fwd.fwdModel(self.lineSource.text(),self.lineStat.text(),self.lineVel2d.text(),self.lineEvent.text(),
                     self.lineRay.text(),self.lineVelout.text(),int(self.split.text()),int(self.biter.text()),
                     int(self.cacah.text()),float(self.pert.text()),progress_callback)
        elt = tac()
        return elt

    def outputClickButtonExecute(self, s):
        file = open(self.lineLog.text(), 'w')
        file.write('Elapsed Time:' + '\t' + s + '\n')

    def errorClickButtonExecute(self):
        self.message = MessageBox()
        self.message.show()

    def completeClickButtonExecute(self):
        self.labstat.setText('Status: Finished')

    def progressClickButtonExecute(self, n):
        self.labstat.setText(n)

    def clickButtonExecute(self):
        # Pass the function to execute
        worker = Worker(
            self.executeClickButtonExecute)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.outputClickButtonExecute)
        worker.signals.error.connect(self.errorClickButtonExecute)
        worker.signals.finished.connect(self.completeClickButtonExecute)
        worker.signals.progress.connect(self.progressClickButtonExecute)

        # Execute
        self.threadpool.start(worker)

    def clickButtonSource(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open source file', '/', "Format File (*.src *.dat)")
        self.lineSource.setText(filepath[0])

    def clickButtonStat(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open station file', '/', "Format File (*.stat *.dat)")
        self.lineStat.setText(filepath[0])

    def clickButtonVel2d(self):
        open = QFileDialog()
        filepath = open.getOpenFileName(self, 'Open 2D velocity file', '/', "Format File (*.vel2d)")
        self.lineVel2d.setText(filepath[0])

    def clickButtonEvent(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save event file', '/', "Format File (*.evt)")
        self.lineEvent.setText(filepath[0])

    def clickButtonRay(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save ray resolution file', '/', "Format File (*.ray2d)")
        self.lineRay.setText(filepath[0])

    def clickButtonVelout(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save 2D velocity file', '/', "Format File (*.vel2d)")
        self.lineVelout.setText(filepath[0])

    def clickButtonLog(self):
        open = QFileDialog()
        filepath = open.getSaveFileName(self, 'Save log file', '/', "Format File (*.log)")
        self.lineLog.setText(filepath[0])

    def setMainTabWidget(self):
        rayView = disp.mainTabRayDisplay()
        self.mainTabWidget.addTab(rayView,'Ray')
        velView = dispV.mainTabRayDisplay()
        self.mainTabWidget.addTab(velView, 'Velocity')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())