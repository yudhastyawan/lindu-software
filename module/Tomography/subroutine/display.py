import numpy as np
from PyQt5 import sip
import vtk

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from traits.api import HasTraits, Instance, on_trait_change, Button
from traitsui.api import View, Item, HGroup, Group
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
import mayavi.mlab as mlab

class Visualization(HasTraits):
    scene1 = Instance(MlabSceneModel, ())
    scene2 = Instance(MlabSceneModel, ())

    button1 = Button('Redraw')
    button2 = Button('Redraw')

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

        self.xx, self.yy, self.zz = np.mgrid[0:nx,0:ny,0:nz]

        self.x = np.zeros(self.xx.shape)
        self.y = np.zeros(self.yy.shape)
        self.z = np.zeros(self.zz.shape)

        for i in range(len(self.xx[:,0,0])):
            for j in range(len(self.xx[0,:,0])):
                for k in range(len(self.xx[0,0,:])):
                    for l in range(nx):
                        if self.xx[i,j,k] == l:
                            self.x[i,j,k] = x[l]

        for i in range(len(self.yy[:,0,0])):
            for j in range(len(self.yy[0,:,0])):
                for k in range(len(self.yy[0,0,:])):
                    for l in range(ny):
                        if self.yy[i,j,k] == l:
                            self.y[i,j,k] = y[l]

        for i in range(len(self.zz[:,0,0])):
            for j in range(len(self.zz[0,:,0])):
                for k in range(len(self.zz[0,0,:])):
                    for l in range(nz):
                        if self.zz[i,j,k] == l:
                            self.z[i,j,k] = z[l]

    @on_trait_change('button1', 'scene.activated')
    def redraw_scene1(self):
        self.redraw_scene(self.scene1)

    @on_trait_change('button2', 'scene.activated')
    def redraw_scene2(self):
        self.redraw_scene3(self.scene2)

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
        scene.mlab.colorbar()
        mlab.axes(ranges=[np.min(x), np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)], figure=scene.mayavi_scene)
        mlab.outline(figure=scene.mayavi_scene)
        # mlab.title('Real View', figure=scene.mayavi_scene)

    def redraw_scene3(self, scene):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.
        xx = self.xx
        yy = self.yy
        zz = self.zz
        vxyz = self.vxyz
        mlab.clf(figure=scene.mayavi_scene)
        s = mlab.volume_slice(xx, yy, zz, vxyz, plane_orientation='x_axes', colormap=self.color, vmin=self.vmin,
                          vmax=self.vmax, figure=scene.mayavi_scene)
        t = mlab.volume_slice(xx, yy, zz, vxyz, plane_orientation='y_axes', colormap=self.color, vmin=self.vmin,
                          vmax=self.vmax, figure=scene.mayavi_scene)
        u = mlab.volume_slice(xx, yy, zz, vxyz, plane_orientation='z_axes', colormap=self.color, vmin=self.vmin,
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
        scene.mlab.colorbar()
        mlab.axes(ranges=[np.min(xx), np.max(xx), np.min(yy), np.max(yy), np.min(zz), np.max(zz)],
                  figure=scene.mayavi_scene)
        mlab.outline(figure=scene.mayavi_scene)
        # mlab.title('Based on Block Number View', figure=scene.mayavi_scene)

    # The layout of the dialog created
    view = View(HGroup(
        Group(
            Item('scene1',
                 editor=SceneEditor(), height=250,
                 width=300),
            'button1',
            show_labels=False,
        ),
        Group(
            Item('scene2',
                 editor=SceneEditor(), height=250,
                 width=300, show_label=False),
            'button2',
            show_labels=False,
        ),
    ),
        resizable=True,
    )


class MainWindow(QMainWindow):
    def __init__(self, logdata, vdata, xdata, ydata, zdata, parent=None):
        super(MainWindow, self).__init__(parent)

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

        self.main_widget = QWidget(self)
        self.vbl = QVBoxLayout(self.main_widget)

        view_button = QPushButton()
        view_button.setText('View Scene')
        view_button.clicked.connect(self.view_click)
        view_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        laybutton = QHBoxLayout()
        laybutton.addWidget(view_button)

        # adding combo box
        self.colormap = QComboBox()
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

        lb_colormap = QLabel()
        lb_colormap.setText('Colormap List')
        lb_colormap.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # adding vmin and vmax
        self.vmin = QLineEdit()
        self.vmin.setText(str(np.min(self.vxyz)))
        lb_vmin = QLabel()
        lb_vmin.setText('Color Min')
        lb_vmin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.vmax = QLineEdit()
        self.vmax.setText(str(np.max(self.vxyz)))
        lb_vmax = QLabel()
        lb_vmax.setText('Color Max')
        lb_vmax.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.check_reverse = QCheckBox()
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
        self.visualization = Visualization(x, y, z, vxyz, self.colormap.currentText(), self.vmin.text(),
                                           self.vmax.text(),0)
        self.ui = self.visualization.edit_traits().control
        self.vbl.addWidget(self.ui)

        self.main_widget.setLayout(self.vbl)
        self.setCentralWidget(self.main_widget)

    def view_click(self):
        if self.check_reverse.isChecked() == False:
            n = 0
        else:
            n = 1
        self.vbl.removeWidget(self.ui)
        sip.delete(self.ui)
        self.ui = None
        self.visualization = Visualization(self.x, self.y, self.z, self.vxyz, self.colormap.currentText(),
                                           self.vmin.text(), self.vmax.text(), n)
        self.ui = self.visualization.edit_traits().control
        self.vbl.addWidget(self.ui)

if __name__ == '__main__':
    logdata = "Z:\Proyek\INOUT\Tomo-real\evt/15real.log"
    vdata = "Z:\Proyek\INOUT\Tomo-real\evt/15vest.vel3d"
    xdata = "Z:\Proyek\INOUT\Tomo-real\evt/15x.data"
    ydata = "Z:\Proyek\INOUT\Tomo-real\evt/15y.data"
    zdata = "Z:\Proyek\INOUT\Tomo-real\evt/15z.data"
    main = MainWindow(logdata,vdata,xdata,ydata,zdata)
    main.show()
    qApp.exec_()