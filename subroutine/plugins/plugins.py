import os
from pyface.qt import QtGui, QtCore
import importlib
from subroutine.thread.threading2 import *
import subprocess

class Plugins(QtGui.QMenu):
    def __init__(self,threadpool,parent=None):
        QtGui.QMenu.__init__(self)
        self.plugMen = []
        self.plugFolds = os.listdir(os.path.join(os.getcwd(),'plugins'))
        self.threadpool = threadpool
        if self.plugFolds != []:
            for i in range(len(self.plugFolds)):
                if os.path.exists(os.path.join(os.getcwd(),'plugins',self.plugFolds[i],'title.txt')):
                    with open(os.path.join(os.getcwd(),'plugins',self.plugFolds[i],'title.txt')) as f:
                        first_line = f.readline()
                else:
                    first_line = self.plugFolds[i]
                self.plugMen.append(QtGui.QAction(first_line,self))
            for i in range(len(self.plugFolds)):
                self.plugMen[i].triggered.connect(lambda x, val=i: self.act_plugins(val))
        self.plugMen.append(self.addSeparator())
        self.plugMen.append(QtGui.QAction("Plugin Custom...", self))
        self.plugMen[-1].triggered.connect(self.act_mCostum)
        for i in self.plugMen:
            self.addAction(i)
        self.installEventFilter(self)
    def act_mCostum(self):
        # Pass the function to execute
        worker = Worker(self.thread_mCostum)
        # Execute
        self.threadpool.start(worker)

    def thread_mCostum(self):
        subprocess.run(r"notepad 'C:\Users\Yudha Styawan\projects\lind-dev\subroutine\plugins\plugins.py'")
        return "Done"

    def act_plugins(self, val):
        module = importlib.import_module('plugins.{}.{}'.format(self.plugFolds[val],self.plugFolds[val]))
        window = module.MainWindow(parent=self)
        window.show()