from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Scroller(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)
    def wheelEvent(self, ev):
        if ev.type() == QEvent.Wheel:
            ev.ignore()