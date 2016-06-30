import os, sys, math, random
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bMapManager import bMap
from bMapManager import bStack
from bMapManager import bStackPlot

class MyWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self.COLORTABLE=[]
		#for i in range(256): self.COLORTABLE.append(QtGui.qRgb(i/4,i,i/2))
		for i in range(256): self.COLORTABLE.append(qRgb(i/4,i,i/2))

		self.map = bMap('a5n')
		self.map.stackList[1].loadtiff()
		a = self.map.stackList[1].getSlice(0)
		self.image = QImage(a.tostring(), a.shape[0], a.shape[1], QImage.Format_Indexed8)
		self.image.setColorTable(self.COLORTABLE)
		print self.image.width(), self.image.height()
		
		self.z = 0
		
		#
		self.setGeometry(100,100,400,400) #set the main window size
		
		self.scene = QGraphicsScene()
		#self.view = QGraphicsView(self.scene)
		self.view = MyGraphicsView(self.scene)
		
		self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

		
		self.imageLabel = QLabel()
		self.imageLabel.setGeometry(10, 10, 400, 400) #position and size of image
		#self.imageLabel.setPixmap(QPixmap(os.getcwd() + "/images/pigeon.png"))
		self.imageLabel.setPixmap(QPixmap.fromImage(self.image))

		self.scene.addWidget(self.imageLabel)
		
		#bug in qt, does not work
		#self.view.translate(10,10)
		
		vbox = QVBoxLayout()
		vbox.addWidget(self.view)

		mainWidget = QWidget()
		mainWidget.setLayout(vbox)

		self.setCentralWidget(mainWidget)

		map = ''
		self.points = DrawingPointsWidget(map)
		self.scene.addWidget(self.points)
		
		self.view.scale(0.5,0.5)
		
		self.points.update() #triggers drawEvent
		
		#self.view.show();
		#self.view.resize(512,512);

	#see:
	#http://stackoverflow.com/questions/16105349/remove-scroll-functionality-on-mouse-wheel-qgraphics-view
	def wheelEvent(self,event):
		print event.delta()
		self.z = self.z + np.sign(event.delta())
		if self.z < 0:
			self.z = 0
		print 'MyWindow.wheelEvent()', self.z
		#self.label.setText("Total Steps: "+QString.number(self.x))

		if self.z >= 0:
			a = self.map.stackList[1].getSlice(self.z)
			if a is not None:
				#print 'wheelEvent()', a.shape, a.dtype
				self.image = QImage(a.tostring(), a.shape[0], a.shape[1], QImage.Format_Indexed8)
				self.image.setColorTable(self.COLORTABLE)
				self.update()
			self.points.z = self.z
			
			#tell points to update, update() will trigger draw !!!
			self.points.update()

class MyGraphicsView(QGraphicsView):
	#def __init__(self, map):
	#	super(QGraphicsView, self).__init__()

	def wheelEvent(self,event):
		#print 'MyGraphicsView.wheelEvent'
		super(MyGraphicsView, self).wheelEvent(event)
		#event.accept()
		
class DrawingPointsWidget(QWidget):
	def __init__(self, map):
		super(QWidget, self).__init__()

		self.map = map
		self.z = 0

		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

		#self.setAttribute(Qt.WA_NoSystemBackground)
		self.setAttribute(Qt.WA_TranslucentBackground)
		#self.setAttribute(Qt.WA_PaintOnScreen)

		#self.setAttribute(Qt.WA_TransparentForMouseEvents);

		self.__setUI()
		
	def __setUI(self):

		self.setGeometry(0, 0, 1024, 1024)
		#self.setWindowTitle('Points')
		self.show()

	def paintEvent(self, e):
		qp = QPainter(self)
		self.drawPoints(qp)

	def drawPoints(self, qp):
		#print 'DrawingPointsWidget::drawPoints()'

		qp.setPen(Qt.blue)
		
		rectWidth = 5
		rectHeight = 5

		#xyz = self.map.stackList[1].getMask(self.z)
		xyz = abs(np.random.random((20,20)) * 100)
		num = len(xyz)
		for i in range(num):
			x = xyz[i][0]
			y = xyz[i][1]
			qp.drawEllipse(x, y, rectWidth, rectHeight)



def main():
	print '=== starting pyqt_stackbrowser'
	app = QApplication(sys.argv)
	window = MyWindow()
	window.show()
	return app.exec_()

if __name__ == '__main__':
	main()