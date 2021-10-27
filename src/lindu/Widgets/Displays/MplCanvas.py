from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import obspy as ob
from PySide2.QtWidgets import QSizePolicy

class MplCanvas(FigureCanvas):
    def __init__(self, path, indexes, parent = None):
        data = ob.read(path)
        n = data.count()

        with plt.rc_context({'axes.edgecolor':'white','xtick.color':'white','ytick.color':'white'}):
            self.fig = Figure()
            self.fig.autofmt_xdate()
            self.fig.patch.set_facecolor((0,0,0))
            self.ax = self.fig.subplots(len(indexes),1,sharex=True)
            self.fig.tight_layout()
            self.fig.subplots_adjust(wspace=0, hspace=0)

            idx = 0
            for i in range(n):
                tr = data.pop(0)
                if i in indexes:
                    if len(indexes) != 1:
                        x = tr.data
                        t = tr.times('matplotlib')
                        self.ax[idx].set_title("seismogram: {}".format(indexes[idx]+1))
                        self.ax[idx].plot(t,x,'r')
                        self.ax[idx].set_facecolor((0,0,0))
                        self.ax[idx].xaxis_date()
                        self.ax[idx].ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
                        idx += 1
                    else:
                        x = tr.data
                        t = tr.times('matplotlib')
                        self.ax.set_title("seismogram: {}".format(indexes[idx]+1))
                        self.ax.plot(t, x, 'r')
                        self.ax.set_facecolor((0, 0, 0))
                        self.ax.xaxis_date()
                        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))


        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)