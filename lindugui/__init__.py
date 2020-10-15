import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
import sys

from pyface.qt import QtGui, QtCore
import vtk
import time
from copy import deepcopy as copy

from lindugui.widgets.main_window import LMainWindow
from lindugui.widgets.menu_bar import LMenu

from lindugui.settings.tictac import tic, tac
from lindugui.settings.threading import Worker, MessageBox, MessageOpt