from pyface.qt import QtGui, QtCore
import traceback, sys
import os

class MessageBox(QtGui.QMessageBox):
    def __init__(self):
        QtGui.QMessageBox.__init__(self)
        self.setWindowTitle('Error !')
        self.icon = QtGui.QIcon(os.path.join(os.getcwd(), 'subroutine', 'icon', 'Icon_Files', 'FIX', 'LOGO.ico'))
        self.setWindowIcon(self.icon)
        self.setText("There is problem with this process")
        self.setInformativeText("Please check it again")
        self.setIcon(QtGui.QMessageBox.Information)
        self.setStandardButtons(QtGui.QMessageBox.Close)

class MessageOpt(QtGui.QMessageBox):
    def __init__(self, title, maintext, opttext):
        QtGui.QMessageBox.__init__(self)
        self.setWindowTitle(title)
        self.icon = QtGui.QIcon(os.path.join(os.getcwd(), 'subroutine', 'icon', 'Icon_Files', 'FIX', 'LOGO.ico'))
        self.setWindowIcon(self.icon)
        self.setText(maintext)
        self.setInformativeText(opttext)
        self.setIcon(QtGui.QMessageBox.Information)
        self.setStandardButtons(QtGui.QMessageBox.Close)

class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            self.signals.error.emit()
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done