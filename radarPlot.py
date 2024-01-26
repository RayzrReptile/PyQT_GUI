import numpy as np
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import sys
import numpy as np
from time import sleep

def addText(plot, degree, x, y):
    text = pg.TextItem(degree)
    plot.addItem(text)
    text.setPos(x, y)

# Setup Window
win = pg.GraphicsLayoutWidget(show=True)
plot = win.addPlot()
plot.setAspectLocked()
plot.setMouseEnabled(x=False, y=False)

# Add polar grid lines
plot.addLine(x=0, pen=0.2)
plot.addLine(y=0, pen=0.2)
for r in range(2, 22, 2):
    circle = QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
    circle.setPen(pg.mkPen(0.2))
    plot.addItem(circle)
    plot.hideAxis('bottom')
    plot.hideAxis('left')

# Add text
addText(plot, "0°", -1, 22)
addText(plot, "45°", 14, 16)
addText(plot, "90°", 20, 1)
addText(plot, "135°", 14, -14)
addText(plot, "180°", -1, -20)
addText(plot, "225°", -17, -14)
addText(plot, "270°", -23, 1)
addText(plot, "315°", -17, 16)

# Draw initial arrow 
arrow = pg.ArrowItem()
arrow.setStyle(angle=-90, tipAngle=8, tailLen=175)
plot.addItem(arrow)

# Initial Variables
rpm = 0.01 # milliseconds
angle = 0 # assumed starting angle

def rotateAngle():
    global angle, arrow
    
    # Reset Arrow
    plot.removeItem(arrow)
    arrow = pg.ArrowItem()
    arrow.setStyle(angle=angle-90, tipAngle=8, tailLen=175)
    plot.addItem(arrow)
    
    # Iterate through angle
    angle=angle+1
    if (angle==360):
        angle=0
    sleep(rpm)

timer = pg.QtCore.QTimer()
timer.timeout.connect(rotateAngle)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec()