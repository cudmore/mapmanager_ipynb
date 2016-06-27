import os
import sys
from PyQt4.QtGui import *

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
