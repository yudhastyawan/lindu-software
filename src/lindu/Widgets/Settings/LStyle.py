# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QFile
import os

def LStyle(res="LStyle.qss"):
    rc = QFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), res))
    rc.open(QFile.ReadOnly)
    content = rc.readAll().data()
    return str(content, "utf-8")