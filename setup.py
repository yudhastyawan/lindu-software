import os
from cx_Freeze import setup, Executable
import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack
import scipy
import matplotlib

# os.environ['TCL_LIBRARY'] = r'C:\Users\Yudha Styawan\.conda\envs\py36\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\Users\Yudha Styawan\.conda\envs\py36\tcl\tk8.6'
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

scipy_path = os.path.dirname(scipy.__file__) #use this if you are also using scipy in your application

build_exe_options = {"packages": ["pyface.ui.qt4", "tvtk.vtk_module", "tvtk.pyface.ui.wx", "matplotlib.backends.backend_qt4",'pygments.lexers',
                                  'tvtk.pyface.ui.qt4','pyface.qt','pyface.qt.QtGui','pyface.qt.QtCore','numpy','matplotlib','mayavi',
                                  'pkg_resources._vendor'],
                     "include_files": [(str(scipy_path), "scipy"), #for scipy
                    (matplotlib.get_data_path(), "mpl-data"),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                       os.path.join(os.getcwd(),'subroutine/'),
                                       os.path.join(os.getcwd(),'module/'),
                                       os.path.join(os.getcwd(),'bug/'),],
                     "includes":['PyQt4.QtCore','PyQt4.QtGui','mayavi','PyQt4'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }


executables = [
    Executable('main.py', targetName="main.exe",base = 'Win32GUI',)
]

setup(name='main',
      version='1.0',
      description='',
      options = {"build_exe": build_exe_options},
      executables=executables,
      )