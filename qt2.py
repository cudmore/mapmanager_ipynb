#!/usr/bin/env python
# -*- coding: utf-8 -*-

#see
#http://stackoverflow.com/questions/8766584/displayin-an-image-in-a-qgraphicsscene

import os, sys, math, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
from PIL import ImageQt
from PIL import ImageEnhance
import time

class TestWidget(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.scene = QGraphicsScene()
		self.view = QGraphicsView(self.scene)
		self.button = QPushButton("Do test")

		layout = QVBoxLayout()
		layout.addWidget(self.button)
		layout.addWidget(self.view)
		self.setLayout(layout)

		self.button.clicked.connect(self.do_test)

	def do_test(self):
		img = Image.open('images/pigeon.png')
		enhancer = ImageEnhance.Brightness(img)
		for i in range(1, 8):
			img = enhancer.enhance(i)
			self.display_image(img)
			QCoreApplication.processEvents()  # let Qt do his work
			time.sleep(0.5)

	def display_image(self, img):
		self.scene.clear()
		
		w, h = img.size
		self.imgQ = ImageQt.ImageQt(img)  # we need to hold reference to imgQ, or it will crash
		print self.imgQ.format()
		pixMap = QPixmap.fromImage(self.imgQ)
		self.scene.addPixmap(pixMap)
		self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)

		size = self.size()
		
		painter = QPainter(self)
		painter.begin(self)
		for i in range(100):
			x = random.randint(1, size.width()-1)
			y = random.randint(1, size.height()-1)
			painter.drawEllipse(x, y, 5, 5)
		painter.end()
		
		self.scene.update()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	widget = TestWidget()
	widget.resize(640, 480)
	widget.show()

	sys.exit(app.exec_())
