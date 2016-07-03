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
		self.setGeometry(100,100,600,600) #set the main window size
		
		self.scene = QGraphicsScene()
		#self.view = QGraphicsView(self.scene)
		self.view = MyGraphicsView(self.scene)
		
		self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

		self.imageLabel = QLabel()
		self.imageLabel.setGeometry(0, 0, 1024, 1024) #position and size of image
		#self.imageLabel.setPixmap(QPixmap(os.getcwd() + "/images/pigeon.png"))
		self.imageLabel.setPixmap(QPixmap.fromImage(self.image))

		#this will translate QWidget with image
		#self.imageLabel.move(200,200)
		
		self.scene.addWidget(self.imageLabel)
		
		#bug in qt, does not work
		#self.view.translate(10,10)
		
		vbox = QVBoxLayout()
		vbox.addWidget(self.view)

		mainWidget = QWidget()
		mainWidget.setLayout(vbox)

		self.setCentralWidget(mainWidget)

		self.points = DrawingPointsWidget(self.map)
		self.scene.addWidget(self.points)
		
		self.view.scale(0.5,0.5)
		
		self.points.update() #triggers drawEvent
		
		#self.view.show();
		#self.view.resize(512,512);

		#set background color of window
		palette = QPalette()
		palette.setColor(QPalette.Background,Qt.gray)
		self.setPalette(palette)

		self.sizeLabel = QLabel()
		self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
		status = self.statusBar()
		status.setSizeGripEnabled(False)
		status.addPermanentWidget(self.sizeLabel)
		status.showMessage("Ready", 5000)

		editToolbar = self.addToolBar("Edit")
		editToolbar.setObjectName("EditToolBar")
		'''
		self.addActions(editToolbar, (editInvertAction,
				editSwapRedAndBlueAction, editUnMirrorAction,
				editMirrorVerticalAction, editMirrorHorizontalAction))
		'''

		self.zoomSpinBox = QSpinBox()
		self.zoomSpinBox.setRange(1, 400)
		self.zoomSpinBox.setSuffix(" %")
		self.zoomSpinBox.setValue(100)
		self.zoomSpinBox.setToolTip("Zoom the image")
		self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
		self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
		self.connect(self.zoomSpinBox,
					 SIGNAL("valueChanged(int)"), self.showImage) #not sure if self.update() is good idea here?
		editToolbar.addWidget(self.zoomSpinBox)
		
	#this is my function
	def editZoom(self):
		if self.image.isNull():
			return
		percent, ok = QInputDialog.getInteger(self,
				"Image Changer - Zoom", "Percent:",
				self.zoomSpinBox.value(), 1, 400)
		if ok:
			self.zoomSpinBox.setValue(percent)

	#this is my function
	def showImage(self, percent=None):
		if self.z >= 0:
			a = self.map.stackList[1].getSlice(self.z)
			if a is not None:
				self.image = QImage(a.tostring(), a.shape[0], a.shape[1], QImage.Format_Indexed8)
				self.image.setColorTable(self.COLORTABLE)

				if percent is None:
					percent = self.zoomSpinBox.value()
				#print 'percent=', percent
				factor = percent / 100.0
				currentImageWidth = self.image.width() * factor
				currentmageHeight = self.image.height() * factor
				self.image = self.image.scaled(currentImageWidth, currentmageHeight, Qt.KeepAspectRatio)

				self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
				
				self.points.scaleFactor = factor
				
				self.update()

	#this is my function
	def updateStatus(self, message):
		self.statusBar().showMessage(message, 5000)
		#put this back in, this should be history of events
		#self.listWidget.addItem(message)
		'''
		if self.filename is not None:
			self.setWindowTitle("Image Changer - {0}[*]".format(
								os.path.basename(self.filename)))
		'''
		if not self.image.isNull():
			self.setWindowTitle("Image Changer - Unnamed[*]")
		else:
			self.setWindowTitle("Image Changer[*]")
		#self.setWindowModified(self.dirty)
		
	#see:
	#http://stackoverflow.com/questions/16105349/remove-scroll-functionality-on-mouse-wheel-qgraphics-view
	def wheelEvent(self,event):
		self.z = self.z + np.sign(event.delta())
		if self.z < 0:
			self.z = 0
		print 'MyWindow.wheelEvent()', event.delta(), self.z
		#self.label.setText("Total Steps: "+QString.number(self.x))

		self.showImage()
		
		self.points.z = self.z
			
		#tell points to update, update() will trigger draw !!!
		self.points.update()

	def keyPressEvent(self, event):
		print 'window.keyPressEvent:', event.text()
		#use QLabel.setGeometry(h,v,w,h) to pan the image
		#print 'keyPressEvent()'
		panValue = 20
		k = event.text()
		if k == 'l':
			self.imageX -= panValue
			self.imageLabel.move(self.imageLabel.x()-20)
		if k == 'r':
			self.imageX += panValue
			self.imageLabel.move(self.imageLabel.x()+20)
		if k == 'u':
			self.imageY -= panValue
		if k == 'd':
			self.imageY += panValue
			
		self.updateStatus("Key '" + event.text() + "' pressed")

class MyGraphicsView(QGraphicsView):
	#def __init__(self, map):
	#	super(QGraphicsView, self).__init__()

	def wheelEvent(self,event):
		#print 'MyGraphicsView.wheelEvent'
		super(MyGraphicsView, self).wheelEvent(event)
		#event.accept()

	def keyPressEvent(self, event):
		#print 'MyGraphicsView.keyPressEvent:', event.text()
		super(MyGraphicsView, self).keyPressEvent(event)
		
class DrawingPointsWidget(QWidget):
	def __init__(self, map):
		super(QWidget, self).__init__()

		self.map = map
		self.z = 0
		self.image = None
		self.scaleFactor = 1 #fraction of total
		
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

		qp.setPen(QPen(Qt.red, 12, Qt.DashDotLine, Qt.RoundCap));
		#qp.setPen(Qt.red)
		
		rectWidth = 7
		rectHeight = 7

		xyz = self.map.stackList[1].getMask(self.z)
		xyz /= float(self.map.stackList[1].header['voxelx'])
		xyz *= self.scaleFactor
		#xyz = abs(np.random.random((20,20)) * 100)
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