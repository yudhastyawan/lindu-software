import os
from cx_Freeze import setup, Executable
import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack
import scipy
import matplotlib
import shutil
import glob

if os.path.exists(os.path.join(os.getcwd(),'build','exe.win-amd64-3.6')):
    if os.listdir(os.path.join(os.getcwd(),'build','exe.win-amd64-3.6')) == 0:
        os.rmdir(os.path.join(os.getcwd(),'build','exe.win-amd64-3.6'))
    else:
        shutil.rmtree(os.path.join(os.getcwd(),'build','exe.win-amd64-3.6'))

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

scipy_path = os.path.dirname(scipy.__file__) #use this if you are also using scipy in your application
filedir = glob.glob(os.path.join(os.getcwd(),".venv\Lib\site-packages\*.*"))
build_exe_options = {"packages": ["pyface.ui.qt4", "tvtk.vtk_module", "tvtk.pyface.ui.wx", "matplotlib.backends.backend_qt4",'pygments.lexers',
                                  'tvtk.pyface.ui.qt4','pyface.qt','pyface.qt.QtGui','pyface.qt.QtCore','numpy','matplotlib','mayavi',
                                  'pyproj','geos','obspy','pkg_resources._vendor'],
                     "include_files": [(str(scipy_path), "scipy"), #for scipy
                    (matplotlib.get_data_path(), "mpl-data"),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                       os.path.join(os.getcwd(),'subroutine/'),
                                       os.path.join(os.getcwd(), 'modules/'),
                                       os.path.join(os.getcwd(),'bug/'),
                                       os.path.join(os.getcwd(),'plugins/'),
                                       os.path.join(os.getcwd(),'tests/'),
                                       os.path.join(os.getcwd(),'lindulib/'),
                                       os.path.join(os.getcwd(),'lindugui/'),
                                       os.path.join(os.getcwd(),'.venv','Lib','site-packages','mpl_toolkits/'),
                                       os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages', 'obspy/'),
                                       os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages', 'requests/'),
                                       os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages', 'idna/'),
                                       os.path.join(os.getcwd(),'.venv','Lib','site-packages','matplotlib/'),]+filedir,
                     "includes":['PyQt4.QtCore','PyQt4.QtGui','mayavi','PyQt4'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }


executables = [
    Executable('main.py', targetName="LindSoft.exe",base = "Win32GUI",
               icon=os.path.join(os.getcwd(),'lindugui/images/icon/main_logo.ico'),)
]

setup(name='Lindu Software',
      version='0.1.0',
      description='Open-Source software for seismological data processing: determining and relocating hypocenter; traveltime tomography',
      options = {"build_exe": build_exe_options},
      executables=executables,
      )