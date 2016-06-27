#20160626
#Author: Robert H Cudmore
#Web: http://robertcudmore.org
#

'''
to draw points, derive a class from QWidget::DrawingPointsWidget and it will have its own paintEvent()
#
points = DrawingPointsWidget
#install this object into main window with addWidget(points)
xxx.addWidget(points)
see:
http://stackoverflow.com/questions/28050397/eventfilter-on-a-qwidget-with-pyqt4
'''

import os, sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		'''
		self.label = QLabel("No data")
		self.label.setGeometry(100, 200, 100, 100)
		self.setCentralWidget(self.label)
		self.setWindowTitle("QMainWindow WheelEvent")
		'''
		self.x = 0
		self.imageX = 0
		self.imageY = 0
		self.imageWidth = 200
		self.imageHeight = 200
		
		#this is required here AND in self.centralWidget()
		self.setMouseTracking(True)

		self.image = QImage('./pigeon.jpg')
		self.dirty = False
		self.filename = 'pigeon xxx'
		self.mirroredvertically = False
		self.mirroredhorizontally = False

		self.move(100,100)
		
		self.imageLabel = QLabel() #for some reason, QLabel is used to diaply images (in general)
		self.imageLabel.setMinimumSize(450, 450)
		self.imageLabel.setAlignment(Qt.AlignCenter)
		self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
		#self.setCentralWidget(self.imageLabel)

		'''
		'''
		mainWidget = QWidget()
		vbox = QVBoxLayout()

		button = QPushButton("Hello")
		vbox.addWidget( button )

		self.points = DrawingPointsWidget()
		self.points.resize(600,600)
		
		vbox.addWidget(self.points)
		vbox.addWidget(self.imageLabel)

		mainWidget.setLayout(vbox)
		self.setCentralWidget(mainWidget)
		'''
		'''
				
		#set background color of window
		palette = QPalette()
		palette.setColor(QPalette.Background,Qt.gray)
		self.setPalette(palette)


		#???
		self.centralWidget().setMouseTracking(True)
		
		#i want to turn on mouse tracking
		#see: http://stackoverflow.com/questions/25368295/qwidgetmousemoveevent-not-firing-when-cursor-over-child-widget
		#self.imageLabel.setMouseTracking(True)

		self.sizeLabel = QLabel()
		self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
		status = self.statusBar()
		status.setSizeGripEnabled(False)
		status.addPermanentWidget(self.sizeLabel)
		status.showMessage("Ready", 5000)

		editInvertAction = self.createAction("&Invert",
				self.editInvert, "Ctrl+I", "editinvert",
				"Invert the image's colors", True, "toggled(bool)")
		editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue",
				self.editSwapRedAndBlue, "Ctrl+A", "editswap",
				"Swap the image's red and blue color components", True,
				"toggled(bool)")
		editZoomAction = self.createAction("&Zoom...", self.editZoom,
				"Alt+Z", "editzoom", "Zoom the image")
		mirrorGroup = QActionGroup(self)
		editUnMirrorAction = self.createAction("&Unmirror",
				self.editUnMirror, "Ctrl+U", "editunmirror",
				"Unmirror the image", True, "toggled(bool)")
		mirrorGroup.addAction(editUnMirrorAction)
		editMirrorHorizontalAction = self.createAction(
				"Mirror &Horizontally", self.editMirrorHorizontal,
				"Ctrl+H", "editmirrorhoriz",
				"Horizontally mirror the image", True, "toggled(bool)")
		mirrorGroup.addAction(editMirrorHorizontalAction)
		editMirrorVerticalAction = self.createAction(
				"Mirror &Vertically", self.editMirrorVertical,
				"Ctrl+V", "editmirrorvert",
				"Vertically mirror the image", True, "toggled(bool)")
		mirrorGroup.addAction(editMirrorVerticalAction)
		editUnMirrorAction.setChecked(True)

		editMenu = self.menuBar().addMenu("&Edit")
		self.addActions(editMenu, (editInvertAction, editSwapRedAndBlueAction, editZoomAction))

		editToolbar = self.addToolBar("Edit")
		editToolbar.setObjectName("EditToolBar")
		self.addActions(editToolbar, (editInvertAction,
				editSwapRedAndBlueAction, editUnMirrorAction,
				editMirrorVerticalAction, editMirrorHorizontalAction))
		#remove this
		#editToolbar.setMouseTracking(True)

		self.zoomSpinBox = QSpinBox()
		self.zoomSpinBox.setRange(1, 400)
		self.zoomSpinBox.setSuffix(" %")
		self.zoomSpinBox.setValue(100)
		self.zoomSpinBox.setToolTip("Zoom the image")
		self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
		self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
		self.connect(self.zoomSpinBox,
					 SIGNAL("valueChanged(int)"), self.showImage)
		editToolbar.addWidget(self.zoomSpinBox)

		self.addActions(self.imageLabel, (editInvertAction,
				editSwapRedAndBlueAction, editUnMirrorAction,
				editMirrorVerticalAction, editMirrorHorizontalAction))

		self.label = QLabel("No data")
		#self.label.setGeometry(100, 200, 100, 100)
		#self.setCentralWidget(self.label)
		#self.setWindowTitle("QMainWindow WheelEvent")
		editToolbar.addWidget(self.label)

		#self.showImage()
		
	def createAction(self, text, slot=None, shortcut=None, icon=None,
					 tip=None, checkable=False, signal="triggered()"):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/{0}.png".format(icon)))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			self.connect(action, SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action


	def addActions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)

	def showImage(self, percent=None):
		if self.image.isNull():
			return
		if percent is None:
			percent = 100 #self.zoomSpinBox.value()
		factor = percent / 100.0
		width = self.image.width() * factor
		height = self.image.height() * factor
		image = self.image.scaled(width, height, Qt.KeepAspectRatio)
		
		image.setOffset(QPoint(100,100))
		self.imageLabel.setPixmap(QPixmap.fromImage(image))
		#??
		#self.imageLabel.setGeometry(self.imageX,self.imageY,self.imageWidth,self.imageHeight)
		
	def editInvert(self, on):
		if self.image.isNull():
			return
		self.image.invertPixels()
		self.showImage()
		self.dirty = True
		self.updateStatus("Inverted" if on else "Uninverted")

	def editSwapRedAndBlue(self, on):
		if self.image.isNull():
			return
		self.image = self.image.rgbSwapped()
		self.showImage()
		self.dirty = True
		self.updateStatus(("Swapped Red and Blue"
						   if on else "Unswapped Red and Blue"))

	def editUnMirror(self, on):
		if self.image.isNull():
			return
		if self.mirroredhorizontally:
			self.editMirrorHorizontal(False)
		if self.mirroredvertically:
			self.editMirrorVertical(False)


	def editMirrorHorizontal(self, on):
		if self.image.isNull():
			return
		self.image = self.image.mirrored(True, False)
		self.showImage()
		self.mirroredhorizontally = not self.mirroredhorizontally
		self.dirty = True
		self.updateStatus(("Mirrored Horizontally"
						   if on else "Unmirrored Horizontally"))

	def editMirrorVertical(self, on):
		if self.image.isNull():
			return
		self.image = self.image.mirrored(False, True)
		self.showImage()
		self.mirroredvertically = not self.mirroredvertically
		self.dirty = True
		self.updateStatus(("Mirrored Vertically"
						   if on else "Unmirrored Vertically"))

	def editZoom(self):
		if self.image.isNull():
			return
		percent, ok = QInputDialog.getInteger(self,
				"Image Changer - Zoom", "Percent:",
				self.zoomSpinBox.value(), 1, 400)
		if ok:
			self.zoomSpinBox.setValue(percent)

	def updateStatus(self, message):
		self.statusBar().showMessage(message, 5000)
		#put this back in, this should be history of events
		#self.listWidget.addItem(message)
		if self.filename is not None:
			self.setWindowTitle("Image Changer - {0}[*]".format(
								os.path.basename(self.filename)))
		elif not self.image.isNull():
			self.setWindowTitle("Image Changer - Unnamed[*]")
		else:
			self.setWindowTitle("Image Changer[*]")
		self.setWindowModified(self.dirty)

	def keyPressEvent(self, event):
		#use QLabel.setGeometry(h,v,w,h) to pan the image
		#print 'keyPressEvent()'
		panValue = 20
		k = event.text()
		if k == 'l':
			self.imageX -= panValue
		if k == 'r':
			self.imageX += panValue
		if k == 'u':
			self.imageY -= panValue
		if k == 'd':
			self.imageY += panValue
			
		#self.imageLabel.setGeometry(100,100,200,200)
		self.showImage()
		self.updateStatus("Key '" + event.text() + "' pressed")
		
	def wheelEvent(self,event):
		self.x =self.x + event.delta()/120
		#print self.x
		self.label.setText("Total Steps: "+QString.number(self.x))

	def mouseMoveEvent(self, event):
		#event: QMouseMoveEvent
		#see: http://pyqt.sourceforge.net/Docs/PyQt4/qwidget.html#mouseMoveEvent
		#print event.pos()
		print 'mouseMoveEvent: x=%d, y=%d' % (event.x(), event.y())
		#self.updateStatus('mouseMoveEvent ' + str(event.x()) + ',' + str(event.y()))

	def mousePressEvent(self, QMouseEvent):
		print 'mousePressEvent:', QMouseEvent.pos()

	def mouseReleaseEvent(self, QMouseEvent):
		cursor = QCursor()
		print 'mouseReleaseEvent:', cursor.pos()		

	#try and draw an image overlay
	def paintEvent(self, e):
		#print 'paintEvent():', e

		#painter = QPainter(self)

		#self.imageLabel.setPixmap(QPixmap.fromImage(image))
		
		#self.showImage()
		
		#painter.drawImage(0,0, QPixmap.fromImage(self.image))
		
		'''
		qp = QPainter(self)
		qp.begin(self)
		qp.drawImage(0,0,self.image)
		#self.drawPoints(qp)
		qp.end()
		'''

		#this was working
		#self.drawPoints(painter)
		
	def drawPoints(self, painter):
	  
		#self.myPainter.begin(self)

		#qp.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
		painter.setPen(QPen(Qt.red,5))
		size = self.size()
		
		for i in range(1000):
			x = random.randint(1, size.width()-1)
			y = random.randint(1, size.height()-1)
			painter.drawPoint(x, y)	 

		#self.myPainter.end(self)

class DrawingPointsWidget(QWidget):
	def __init__(self):
		super(QWidget, self).__init__()
		self.__setUI()

	def __setUI(self):

		self.setGeometry(300, 300, 280, 170)
		self.setWindowTitle('Points')
		self.show()

	def paintEvent(self, e):
		#qp = QtGui.QPainter()
		qp = QPainter()
		qp.begin(self)
		self.drawPoints(qp)
		qp.end()

	def drawPoints(self, qp):
		#print 'DrawingPointsWidget::drawPoints()'
		
		qp.setPen(Qt.red)

		size = self.size()
		
		for i in range(1000):
			x = random.randint(1, size.width()-1 )
			y = random.randint(1, size.height()-1 )
			qp.drawPoint(x, y)
		
def main():
	print '=== starting pyqt_stackbrowser'
	app = QApplication(sys.argv)
	window = MyWindow()
	window.show()
	return app.exec_()

if __name__ == '__main__':
	main()