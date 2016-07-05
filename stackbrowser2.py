import os, sys, math, random
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pyqtgraph as pg

from bMapManager import bMap
from bMapManager import bStack
from bMapManager import bStackPlot

class MyWindow2(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)

class MyWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setWindowTitle('Stack Browser 2')

		#a second window (works)
		#self.secondWindow = MyWindow2(self)
		#self.secondWindow.show()
		
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

		'''
		self.setMouseTracking(True)
		self.installEventFilter(self)
		'''
		
		self.view.setMouseTracking(True)
		self.view.viewport().installEventFilter(self)
		#this is required otherwise QGraphicsView eats arrow keys (does not eat other keys)
		self.view.installEventFilter(self)
		
		#turn of scrollbar
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		
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
		
		#button to show/hide left toolbar
		self.myButtonID1 = QPushButton('Left Toolbar')
		self.myButtonID1.clicked.connect(lambda:self.myButtonPress(self.myButtonID1))
		editToolbar.addWidget(self.myButtonID1)

		#ch1 button
		self.myCh1ButtonID = QPushButton('Channel 1')
		self.myCh1ButtonID.clicked.connect(lambda:self.myButtonPress(self.myCh1ButtonID))
		editToolbar.addWidget(self.myCh1ButtonID)
		#ch2 button
		self.myCh2ButtonID = QPushButton('Channel 2')
		self.myCh2ButtonID.clicked.connect(lambda:self.myButtonPress(self.myCh2ButtonID))
		editToolbar.addWidget(self.myCh2ButtonID)

		#button to plot
		self.myButtonID2 = QPushButton('Plot 1')
		self.myButtonID2.clicked.connect(lambda:self.myButtonPress(self.myButtonID2))
		editToolbar.addWidget(self.myButtonID2)

		#checkbox to show/hide tracong
		self.checkbox1 = QCheckBox('Show Tracing')
		self.checkbox1.stateChanged.connect(lambda:self.myButtonPress(self.checkbox1))
		editToolbar.addWidget(self.checkbox1)

		#todo: put this into Qt.LeftToolBarArea
		self.leftToolbar = QToolBar('left_tb')
		self.addToolBar(Qt.LeftToolBarArea, self.leftToolbar)

		#list for stack db
		self.list = QTableView(self) #uses model/view
		spinesModel = PandasModel(self.map.stackList[1].getSpines())
		self.list.setModel(spinesModel)
		self.list.setFont(QFont("Arial", 10))
		self.leftToolbar.addWidget(self.list)
		#self.leftToolbar.setVisible(True)
		
	def myButtonPress(self,b):
		#print "clicked button is "+b.text()
		button = b.text()
		if button == 'Left Toolbar':
			self.leftToolbar.setVisible(not self.leftToolbar.isVisible())
		elif button == 'Show Tracing':
			self.points.isVisible = b.isChecked()
			self.update()
		elif button=='Plot 1':
			self.myPlot()
		elif button=='Channel 1':
			self.map.stackList[1].currentChannel = 1
		elif button=='Channel 2':
			self.map.stackList[1].currentChannel = 2
						
	def myPlot(self):
		spines = self.map.stackList[1].getSpines()
		x = spines.x.values
		y = spines.y.values
		pg.plot(x, y, pen=None, symbol='o')
	
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
		
	def eventFilter(self, source, event):
		if (event.type() == QEvent.Wheel or event.type()==QEvent.GraphicsSceneWheel):
			self.wheelEvent(event)
			return 1
			
		if (event.type() == QEvent.MouseMove and
			source is self.view.viewport()):
			pos = event.pos()
			#print('mouse move: (%d, %d)' % (pos.x(), pos.y()))
			self.updateStatus('mouse ' + str(pos.x()) + ' ' + str(pos.y()))
			return 1
			
		if (event.type() == QEvent.KeyPress):
			#self.updateStatus('mouse ' + str(pos.x()) + ' ' + str(pos.y()))
			self.keyPressEvent(event)
			return 1
			
		return QMainWindow.eventFilter(self, source, event)

	#see:
	#http://stackoverflow.com/questions/16105349/remove-scroll-functionality-on-mouse-wheel-qgraphics-view
	def wheelEvent(self,event):
		self.z = self.z + np.sign(event.delta())
		if self.z < 0:
			self.z = 0
		#print 'MyWindow.wheelEvent()', event.delta(), self.z
		#self.label.setText("Total Steps: "+QString.number(self.x))

		self.showImage()
		
		self.points.z = self.z
			
		#tell points to update, update() will trigger draw !!!
		self.points.update()

	def keyPressEvent(self, event):
		#print 'window.keyPressEvent:', event.text()
		#use QLabel.setGeometry(h,v,w,h) to pan the image
		#print 'keyPressEvent()'
		panValue = 20
		k = event.key()
		self.updateStatus("Key '" + event.text() + "' " + str(event.key()) + " pressed")
		if k == Qt.Key_Left:
			#self.imageX -= panValue
			self.imageLabel.move(self.imageLabel.x()-20,self.imageLabel.y())
		if k == Qt.Key_Right:
			#self.imageX += panValue
			self.imageLabel.move(self.imageLabel.x()+20,self.imageLabel.y())
		if k == Qt.Key_Up:
			#self.imageY -= panValue
			self.imageLabel.move(self.imageLabel.x(),self.imageLabel.y()-20)
		if k == Qt.Key_Down:
			#self.imageY += panValue
			self.imageLabel.move(self.imageLabel.x(),self.imageLabel.y()+20)
		if k==Qt.Key_Enter or k==Qt.Key_Return:
			print 'rest image to full view and center'
			self.imageLabel.move(0,0)
		self.update()

class PandasModel(QAbstractTableModel):
	"""
	Class to populate a table view with a pandas dataframe
	"""
	def __init__(self, data, parent=None):
		QAbstractTableModel.__init__(self, parent)
		self._data = data

	def rowCount(self, parent=None):
		return len(self._data.values)

	def columnCount(self, parent=None):
		return self._data.columns.size

	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():
			if role == Qt.DisplayRole:
				return str(self._data.values[index.row()][index.column()])
		return None

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self._data.columns[col]
		return None
		
class MyGraphicsView(QGraphicsView):
	pass
	#def __init__(self, map):
	#	super(QGraphicsView, self).__init__()

	'''
	def eventFilter(self, source, event):
		if (event.type() == QEvent.MouseMove):
			pos = event.pos()
			print('MyGraphicsView mouse move: (%d, %d)' % (pos.x(), pos.y()))
		return QGraphicsView.eventFilter(self, source, event)

	def wheelEvent(self,event):
		#print 'MyGraphicsView.wheelEvent'
		super(MyGraphicsView, self).wheelEvent(event)
		#event.accept()

	def keyPressEvent(self, event):
		print 'MyGraphicsView.keyPressEvent:', event.text(), event.key()
		super(MyGraphicsView, self).keyPressEvent(event)
	'''
		
class DrawingPointsWidget(QWidget):
	def __init__(self, map):
		super(QWidget, self).__init__()

		self.map = map
		self.z = 0
		self.image = None
		self.scaleFactor = 1 #fraction of total
		self.isVisible = 1
		
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

		if not self.isVisible:
			return
		
		qp.setPen(QPen(Qt.red, 12, Qt.DashDotLine, Qt.RoundCap));
		
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