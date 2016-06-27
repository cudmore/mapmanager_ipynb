import os, sys, random
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import * #QPixmap, QLabel, QImage
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		
		#self.pixmap = QPixmap(os.getcwd() + '/pigeon.jpg')
		self.pixmap = QImage(os.getcwd() + '/pigeon.jpg')
		#self.label = QLabel(self)
		#self.label.setPixmap(self.pixmap)

		self.initUI()

		
	def initUI(self):	  

		self.setGeometry(200, 200, 300, 300)
		self.setWindowTitle('Points')
		self.show()

	def paintEvent(self, e):

		qp = QtGui.QPainter()
		qp.begin(self)
		qp.drawImage(0,0,self.pixmap)
		self.drawPoints(qp)
		qp.end()
		
	def drawPoints(self, qp):
	  
		#qp.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
		qp.setPen(QtCore.Qt.red)
		size = self.size()
		
		for i in range(10000):
			x = random.randint(1, size.width()-1)
			y = random.randint(1, size.height()-1)
			qp.drawPoint(x, y)	 
				
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

'''
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle("PyQT4 Pixmap @ pythonspot.com ") 
 
# Create widget
label = QLabel(w)
pixmap = QPixmap(os.getcwd() + '/pigeon.jpg')
label.setPixmap(pixmap)
w.resize(pixmap.width()*2,pixmap.height()*2)
 
# Draw window
w.show()
app.exec_()
'''