#!/usr/bin/python -tt

import sys
import numpy
from PyQt4 import QtGui, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Circle

class SelectablePoint:
    def __init__(self, xy, label, fig):
        self.point = Circle( (xy[0], xy[1]), .25, figure=fig)
        self.label = label
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.onClick)

    def onClick(self, e):
        if self.point.contains(e)[0]:
            print self.label


class ScatterPlot(FigureCanvas):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''

        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)

        self.axes = self.fig.add_subplot(111)
        xlim = [0,7]
        ylim = [0,7]
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)
        self.axes.set_aspect( 1 )

        x = [1, 1.2, 3, 4, 5, 6]
        y = [1, 1.2, 3, 4, 5, 6]
        labels = ['1', '2', '3', '4', '5', '6']

        for i in range(len(x)):
            sp = SelectablePoint( (x[i],y[i]), labels[i], self.fig)
            self.axes.add_artist(sp.point)

class MainContainer(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(900,600)
        self.setWindowTitle('Scatter Plot')

        sp = ScatterPlot(self)
        self.setCentralWidget(sp)

        self.center()

    def center(self):
        # Get the resolution of the screen
        screen = QtGui.QDesktopWidget().screenGeometry()

        # Get the size of widget
        size = self.geometry()
        self.move( (screen.width() - size.width())/2, (screen.height() - size.height())/2 )

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    b = MainContainer()
    b.show()
    sys.exit(app.exec_())