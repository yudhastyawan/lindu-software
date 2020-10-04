import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change, Button
from traitsui.api import View, Item, Group
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor
import numpy as np
from mayavi import mlab

################################################################################
#The actual visualization
class Blankvir(HasTraits):
    scene = Instance(MlabSceneModel, ())
    # the layout of the dialog screated
    view = View(Group(
            Item('scene',
                 editor=SceneEditor(scene_class=MayaviScene), height=250,
                 width=300, show_label=False), show_labels=False,),
                resizable=True # We need this to resize with the parent widget
                )


class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    def __init__(self, x, y, z, vxyz, colormap, vmin, vmax, n):
        HasTraits.__init__(self)
        self.vxyz = vxyz
        self.color = colormap
        self.vmin = float(vmin)
        self.vmax = float(vmax)
        self.n = n

        nx = len(x)
        ny = len(y)
        nz = len(z)

        self.xx, self.yy, self.zz = np.mgrid[0:nx, 0:ny, 0:nz]

        self.x = np.zeros(self.xx.shape)
        self.y = np.zeros(self.yy.shape)
        self.z = np.zeros(self.zz.shape)

        for i in range(len(self.xx[:, 0, 0])):
            for j in range(len(self.xx[0, :, 0])):
                for k in range(len(self.xx[0, 0, :])):
                    for l in range(nx):
                        if self.xx[i, j, k] == l:
                            self.x[i, j, k] = x[l]

        for i in range(len(self.yy[:, 0, 0])):
            for j in range(len(self.yy[0, :, 0])):
                for k in range(len(self.yy[0, 0, :])):
                    for l in range(ny):
                        if self.yy[i, j, k] == l:
                            self.y[i, j, k] = y[l]

        for i in range(len(self.zz[:, 0, 0])):
            for j in range(len(self.zz[0, :, 0])):
                for k in range(len(self.zz[0, 0, :])):
                    for l in range(nz):
                        if self.zz[i, j, k] == l:
                            self.z[i, j, k] = z[l]

    @on_trait_change('scene.activated')
    def redraw_scene1(self):
        self.redraw_scene(self.scene)

    def redraw_scene(self, scene):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        x = self.x
        y = self.y
        z = self.z
        vxyz = self.vxyz
        mlab.clf(figure=scene.mayavi_scene)
        s = mlab.volume_slice(x, y, z, vxyz, plane_orientation='x_axes', colormap=self.color, vmin=self.vmin,
                          vmax=self.vmax, figure=scene.mayavi_scene)
        t = mlab.volume_slice(x, y, z, vxyz, plane_orientation='y_axes', colormap=self.color, vmin=self.vmin,
                          vmax=self.vmax, figure=scene.mayavi_scene)
        u = mlab.volume_slice(x, y, z, vxyz, plane_orientation='z_axes', colormap=self.color, vmin=self.vmin,
                          vmax=self.vmax, figure=scene.mayavi_scene)
        if self.n == 1:
            lut = s.module_manager.scalar_lut_manager.lut.table.to_array()
            ilut = lut[::-1]
            s.module_manager.scalar_lut_manager.lut.table = ilut
            lut = t.module_manager.scalar_lut_manager.lut.table.to_array()
            ilut = lut[::-1]
            t.module_manager.scalar_lut_manager.lut.table = ilut
            lut = u.module_manager.scalar_lut_manager.lut.table.to_array()
            ilut = lut[::-1]
            u.module_manager.scalar_lut_manager.lut.table = ilut
        mlab.colorbar(orientation='vertical',title='velocity')
        mlab.axes(ranges=[np.min(x), np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)], figure=scene.mayavi_scene)
        mlab.outline(figure=scene.mayavi_scene)
        # mlab.show_pipeline()
        # mlab.title('Real View', figure=scene.mayavi_scene)

    # the layout of the dialog screated
    view = View(Group(
            Item('scene',
                 editor=SceneEditor(scene_class=MayaviScene), height=250,
                 width=300, show_label=False), show_labels=False,),
                resizable=True # We need this to resize with the parent widget
                )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, logdata, vdata, xdata, ydata, zdata, parent=None):
        QtGui.QWidget.__init__(self, parent)
        themlayout = QtGui.QVBoxLayout(self)
        themlayout.setContentsMargins(0, 0, 0, 0)
        themlayout.setSpacing(0)

        # data
        file = open(logdata, 'r')
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].split()
        file.close()

        nx = int(data[8][-1])
        ny = int(data[9][-1])
        nz = int(data[10][-1])

        vxyz = np.fromfile(vdata)
        vxyz = vxyz.reshape((nx, ny, nz))

        x = np.fromfile(xdata)
        y = np.fromfile(ydata)
        z = np.fromfile(zdata)

        self.x = x
        self.y = y
        self.z = z
        self.vxyz = vxyz

        self.main_widget = QtGui.QWidget(self)
        self.vbl = QtGui.QVBoxLayout(self.main_widget)

        view_button = QtGui.QPushButton()
        view_button.setText('View Scene')
        view_button.clicked.connect(self.view_click)
        view_button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        laybutton = QtGui.QHBoxLayout()
        laybutton.addWidget(view_button)

        # adding combo box
        self.colormap = QtGui.QComboBox()
        self.colormap.addItem('jet')
        self.colormap.addItem('bwr')
        item = ['Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 'Greys', 'OrRd',
                'Oranges', 'PRGn', 'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu', 'PuBuGn', 'PuOr', 'PuRd', 'Purples',
                'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3', 'Spectral', 'Vega10',
                'Vega20', 'Vega20b', 'Vega20c', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'afmhot', 'autumn',
                'binary', 'black-white', 'blue-red', 'bone', 'brg', 'cool', 'coolwarm', 'copper', 'cubehelix', 'file',
                'flag', 'gist_earth', 'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 'gist_stern', 'gist_yarg',
                'gnuplot', 'gnuplot2', 'gray', 'hot', 'hsv', 'inferno', 'magma', 'nipy_spectral', 'ocean', 'pink',
                'plasma', 'prism', 'rainbow', 'seismic', 'spectral', 'spring', 'summer', 'terrain', 'viridis', 'winter']
        for i in range(len(item)):
            self.colormap.addItem(item[i])

        lb_colormap = QtGui.QLabel()
        lb_colormap.setText('Colormap List')
        lb_colormap.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        # adding vmin and vmax
        self.vmin = QtGui.QLineEdit()
        self.vmin.setText(str(np.min(self.vxyz)))
        lb_vmin = QtGui.QLabel()
        lb_vmin.setText('Color Min')
        lb_vmin.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.vmax = QtGui.QLineEdit()
        self.vmax.setText(str(np.max(self.vxyz)))
        lb_vmax = QtGui.QLabel()
        lb_vmax.setText('Color Max')
        lb_vmax.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self.check_reverse = QtGui.QCheckBox()
        self.check_reverse.setText('reverse colormap')

        laybutton.addStretch()
        laybutton.addWidget(lb_vmin)
        laybutton.addWidget(self.vmin)
        laybutton.addWidget(lb_vmax)
        laybutton.addWidget(self.vmax)
        laybutton.addWidget(lb_colormap)
        laybutton.addWidget(self.colormap)
        laybutton.addWidget(self.check_reverse)
        self.vbl.addLayout(laybutton)

        # connect to mayavi
        self.visualization = Blankvir()        # self.visualization.configure_traits()
        # self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        self.vbl.addWidget(self.ui)
        # self.ui.setParent(self)
        self.main_widget.setLayout(self.vbl)
        themlayout.addWidget(self.main_widget)

    def view_click(self):
        if self.check_reverse.isChecked() == False:
            n = 0
        else:
            n = 1
        # self.visualization.edit_traits().dispose()
        # self.ui = None
        # self.vbl.removeWidget(self.ui)
        # sip.delete(self.ui)
        # self.visualization = None
        self.visualization.scene.mayavi_scene.remove()
        self.ui.close()
        self.visualization = Visualization(self.x, self.y, self.z, self.vxyz, self.colormap.currentText(),
                                           self.vmin.text(), self.vmax.text(), n)
        # self.visualization.configure_traits()
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        # self.ui.show()
        self.vbl.addWidget(self.ui)
        # self.ui.setParent(self)

    def closeEvent(self, event):
        self.ui.close()

if __name__ == "__main__":

    logdata = "Z:\Proyek\INOUT\Tomo-real\evt/15real.log"
    vdata = "Z:\Proyek\INOUT\Tomo-real\evt/15vest.vel3d"
    xdata = "Z:\Proyek\INOUT\Tomo-real\evt/15x.data"
    ydata = "Z:\Proyek\INOUT\Tomo-real\evt/15y.data"
    zdata = "Z:\Proyek\INOUT\Tomo-real\evt/15z.data"
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QtGui.QApplication.instance()
    # container = QtGui.QWidget()

    mayavi_widget = MayaviQWidget(logdata,vdata,xdata,ydata,zdata)

    # container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
    # # define a "complex" layout to test the behaviour
    # layout = QtGui.QHBoxLayout(container)
    #
    # button_container = QtGui.QWidget()
    # button_layout =  QtGui.QVBoxLayout(button_container)

    # button1 = QtGui.QPushButton('1')
    # button1.clicked.connect(mayavi_widget.visualization.update_plot)
    # button_layout.addWidget(button1)
    #
    # button2 = QtGui.QPushButton('2')
    # button2.clicked.connect(mayavi_widget.visualization.second_plot)
    # button_layout.addWidget(button2)
    #
    # button3 = QtGui.QPushButton('3')
    # button3.clicked.connect(mayavi_widget.visualization.third_plot)
    # button_layout.addWidget(button3)

    # layout.addWidget(button_container)
    # button_container.show()

    # layout.addWidget(mayavi_widget)
    # container.show()
    # window = QtGui.QMainWindow()
    # window.setCentralWidget(container)
    mayavi_widget.show()

    # Start the main event loop.
    app.exec_()