from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import traceback, sys
import os

class MessageBox(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.setWindowTitle('Error !')
        self.setWindowIcon(self.icon)
        self.setText("There is problem with this process")
        self.setInformativeText("Please check it again")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Close)

class MessageOpt(QMessageBox):
    def __init__(self, title, maintext, opttext):
        QMessageBox.__init__(self)
        self.setWindowTitle(title)
        self.setWindowIcon(self.icon)
        self.setText(maintext)
        self.setInformativeText(opttext)
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Close)

class WorkerSignals(QObject):
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
    finished = Signal()
    error = Signal()
    result = Signal(object)
    progress = Signal(object)


class Worker(QRunnable):
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

    @Slot()
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