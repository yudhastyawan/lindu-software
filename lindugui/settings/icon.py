import os
from pyface.qt.QtGui import QIcon

mainpath = os.path.split(os.path.dirname(__file__))[0]
iconpath = os.path.join(mainpath,'images','icon')
largespath = os.path.join(mainpath,'images','larges')

class icon(object):
    main_logo = os.path.join(iconpath,'main_logo.png')
    splash_screen = os.path.join(largespath, 'spl_scr.png')

class LIcon(QIcon):
    def __init__(self, parent = None):
        super(LIcon, self).__init__(parent)