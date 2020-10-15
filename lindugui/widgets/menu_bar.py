from pyface.qt.QtGui import QAction

class LMenu:
    @staticmethod
    def addMenu(name, mbar, disabled=False):
        Name = mbar.addMenu(name)
        if disabled == True:
            Name.setDisabled(True)
        else:
            pass
        return Name

    @staticmethod
    def addAction(name, mbar, disabled=False, triggered=None):
        Name = mbar.addAction(name)
        if disabled == True:
            Name.setDisabled(True)
        else:
            pass
        if triggered == None:
            pass
        else:
            Name.triggered.connect(triggered)
        return Name

    @staticmethod
    def insertAction(name, widget, mbar, mBefore, disabled=False, triggered=None):
        Name = QAction(widget)
        Name.setText(name)
        mbar.insertAction(mBefore, Name)
        if disabled == True:
            Name.setDisabled(True)
        else:
            pass
        if triggered == None:
            pass
        else:
            Name.triggered.connect(triggered)
        return Name