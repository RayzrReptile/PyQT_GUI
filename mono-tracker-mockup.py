'''
Peyton Adkins
January 22nd, 2024

The following code is a mockup GUI program that showcases the possibilities of the PyQT library as well as the ease of use of QT Designer. The main phased array beamforming algorithm, formerly titled the Monopulse Tracker, was originally developed by Jon Kraft. His policy of use is written below.

Acknowledgments to colleague Joel Brigida for his contributions to the beamforming code modifications to better suit our project specifications.

Jon Kraft, Nov 5 2022
https://github.com/jonkraft/Pluto_Beamformer
video walkthrough of this at:  https://www.youtube.com/@jonkraft

'''
# Copyright (C) 2020 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np
import sys
import adi
print(f'sys.path = {sys.path}') 

'''Define UI Window Class'''
class Ui_MainWindow(object):
    def toggleTracker(self):
        text = self.toggleTrackerButton.text()
        if text == 'Tracking: ON':
            self.toggleTrackerButton.setText("Tracking: OFF")
            self.RxDial.setEnabled(True)
            self.TxDial.setEnabled(True)
            self.phaseCalibration.setEnabled(True)
        elif text == 'Tracking: OFF':
            self.toggleTrackerButton.setText("Tracking: ON")
            self.RxDial.setEnabled(False)
            self.TxDial.setEnabled(False)
            self.phaseCalibration.setEnabled(False)
        
    def getToggle(self):
        text = self.toggleTrackerButton.text()
        if text == 'Tracking: ON':
            return True
        elif text == 'Tracking: OFF':
            return False

    def adjustRX(self):
        rxVal = self.RxDial.value()
        self.labelRxGain.setText(str(rxVal))

    def getRXGain(self):
        return self.RxDial.value()

    def adjustTX(self):
        txVal = self.TxDial.value()
        self.labelTxGain.setText(str(txVal))

    def getTXGain(self):
        return self.TxDial.value()

    def getPhaseCal(self):
        return self.phaseCalibration.value()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.trackerView = GraphicsLayoutWidget(self.centralwidget)
        self.trackerView.setGeometry(QtCore.QRect(20, 20, 511, 401))
        self.trackerView.setObjectName("trackerView")

        self.RxDial = QtWidgets.QDial(self.centralwidget)
        self.RxDial.setGeometry(QtCore.QRect(140, 440, 91, 81))
        self.RxDial.setObjectName("RxDial")
        self.RxDial.setValue(60)
        self.RxDial.setMinimum(0)
        self.RxDial.setMaximum(60)
        self.RxDial.valueChanged.connect(self.adjustRX)
        self.RxDial.setEnabled(False)

        self.TxDial = QtWidgets.QDial(self.centralwidget)
        self.TxDial.setGeometry(QtCore.QRect(240, 440, 91, 81))
        self.TxDial.setObjectName("TxDial")
        self.TxDial.setValue(0)
        self.TxDial.setMinimum(0)
        self.TxDial.setMaximum(60)
        self.TxDial.valueChanged.connect(self.adjustTX)
        self.TxDial.setEnabled(False)

        self.phaseCalibration = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.phaseCalibration.setGeometry(QtCore.QRect(350, 480, 101, 31))
        self.phaseCalibration.setMinimum(-180.0)
        self.phaseCalibration.setMaximum(180.0)
        self.phaseCalibration.setSingleStep(1.0)
        self.phaseCalibration.setObjectName("phaseCalibration")
        self.phaseCalibration.setEnabled(False)

        self.labelPhaseCal = QtWidgets.QLabel(self.centralwidget)
        self.labelPhaseCal.setGeometry(QtCore.QRect(350, 460, 121, 16))
        self.labelPhaseCal.setObjectName("labelPhaseCal")

        self.labelDial1 = QtWidgets.QLabel(self.centralwidget)
        self.labelDial1.setGeometry(QtCore.QRect(150, 430, 71, 16))
        self.labelDial1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDial1.setObjectName("labelDial1")

        self.labelDial2 = QtWidgets.QLabel(self.centralwidget)
        self.labelDial2.setGeometry(QtCore.QRect(250, 430, 71, 16))
        self.labelDial2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDial2.setObjectName("labelDial2")

        self.firstWidget = GraphicsLayoutWidget(self.centralwidget)
        self.firstWidget.setGeometry(QtCore.QRect(545, 20, 231, 201))
        self.firstWidget.setObjectName("firstWidget")

        self.secondWidget = GraphicsLayoutWidget(self.centralwidget)
        self.secondWidget.setGeometry(QtCore.QRect(545, 230, 231, 191))
        self.secondWidget.setObjectName("secondWidget")

        self.toggleTrackerButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleTrackerButton.setGeometry(QtCore.QRect(20, 440, 111, 91))
        self.toggleTrackerButton.setObjectName("toggleTrackerButton")
        self.toggleTrackerButton.clicked.connect(self.toggleTracker)

        self.labelRxGain = QtWidgets.QLabel(self.centralwidget)
        self.labelRxGain.setGeometry(QtCore.QRect(150, 520, 71, 16))
        self.labelRxGain.setAlignment(QtCore.Qt.AlignCenter)
        self.labelRxGain.setObjectName("labelRxGain")

        self.labelTxGain = QtWidgets.QLabel(self.centralwidget)
        self.labelTxGain.setGeometry(QtCore.QRect(250, 520, 71, 16))
        self.labelTxGain.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTxGain.setObjectName("labelTxGain")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionThis_is_an_option = QtWidgets.QAction(MainWindow)
        self.actionThis_is_an_option.setObjectName("actionThis_is_an_option")
        self.actionA_second_option = QtWidgets.QAction(MainWindow)
        self.actionA_second_option.setObjectName("actionA_second_option")
        self.actionAnd_so_on = QtWidgets.QAction(MainWindow)
        self.actionAnd_so_on.setObjectName("actionAnd_so_on")
        self.menuFile.addAction(self.actionThis_is_an_option)
        self.menuFile.addAction(self.actionA_second_option)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAnd_so_on)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelPhaseCal.setText(_translate("MainWindow", "Phase Calibration"))
        self.labelDial1.setText(_translate("MainWindow", "Rx Gain"))
        self.labelDial2.setText(_translate("MainWindow", "Tx Gain"))
        self.toggleTrackerButton.setText(_translate("MainWindow", "Tracking: ON"))
        self.labelRxGain.setText(_translate("MainWindow", "60"))
        self.labelTxGain.setText(_translate("MainWindow", "0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionThis_is_an_option.setText(_translate("MainWindow", "This is an option"))
        self.actionA_second_option.setText(_translate("MainWindow", "A second option"))
        self.actionAnd_so_on.setText(_translate("MainWindow", "And so on"))
    
    def setupTrackerGraph(self, tracking_length):
        p1 = self.trackerView.addPlot()
        p1.setXRange(-80,80)
        p1.setYRange(0, tracking_length)
        p1.setLabel('bottom', 'Steering Angle', 'deg', **{'color': '#FFF', 'size': '14pt'})
        p1.showAxis('left', show=False)
        p1.showGrid(x=True, alpha=1)
        p1.setTitle('Monopulse Tracking:  Angle vs Time', **{'color': '#FFF', 'size': '14pt'})
        fn = QtGui.QFont()
        fn.setPointSize(15)
        p1.getAxis("bottom").setTickFont(fn)
        return p1

    def setupFirstGraph(self):
        p2 = self.firstWidget.addPlot(title="Multiple curves")
        p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
        p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Green curve")
        p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Blue curve")
        return p2

    def setupSecondGraph(self):
        p3 = self.secondWidget.addPlot(title="Updating plot")
        curve = p3.plot(pen='y')
        data = np.random.normal(size=(10,1000))
        ptr = 0
        curve.setData(data[ptr%10])
        if ptr == 0:
            p3.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        ptr += 1
        return p3

'''Setup'''
samp_rate = 2e6    # must be <=30.72 MHz if both channels are enabled
NumSamples = 2**12
rx_lo = 2.3e9
rx_mode = "manual"  # can be "manual" or "slow_attack"
rx_gain0 = 60
rx_gain1 = 60
tx_lo = rx_lo
tx_gain = 0
fc0 = int(200e3)
phase_cal = 0
tracking_length = 1000
signal_start = int(NumSamples*(samp_rate/2+fc0/2)/samp_rate)
signal_end = int(NumSamples*(samp_rate/2+fc0*2)/samp_rate)

''' Set distance between Rx antennas '''
d_wavelength = 0.5                  # distance between elements as a fraction of wavelength.  This is normally 0.5
wavelength = 3E8/rx_lo              # wavelength of the RF carrier
d = d_wavelength*wavelength         # distance between elements in meters
print("Set distance between Rx Antennas to ", int(d*1000), "mm")

''' Create Radio '''
sdr = adi.ad9361(uri='ip:192.168.2.1')

''' Configure properties for the Rx Pluto '''
def setupPluto(samp_rate, fc0, rx_lo, rx_mode, rx_gain0, rx_gain1, NumSamples, tx_lo, tx_gain):
    sdr.rx_enabled_channels = [0, 1]
    sdr.sample_rate = int(samp_rate)
    sdr.rx_rf_bandwidth = int(fc0*3)
    sdr.rx_lo = int(rx_lo)
    sdr.gain_control_mode = rx_mode
    sdr.rx_hardwaregain_chan0 = int(rx_gain0)
    sdr.rx_hardwaregain_chan1 = int(rx_gain1)
    sdr.rx_buffer_size = int(NumSamples)
    sdr._rxadc.set_kernel_buffers_count(1)   # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
    sdr.tx_rf_bandwidth = int(fc0*3)
    sdr.tx_lo = int(tx_lo) #make same as rx_lo
    sdr.tx_cyclic_buffer = True
    sdr.tx_hardwaregain_chan0 = int(tx_gain)
    sdr.tx_hardwaregain_chan1 = int(-88)
    sdr.tx_buffer_size = int(2**18)

setupPluto(samp_rate, fc0, rx_lo, rx_mode, rx_gain0, rx_gain1, NumSamples, tx_lo, tx_gain)

''' Program Tx and Send Data '''
def programTX(sdr):
    fs = int(sdr.sample_rate)
    N = 2**16
    ts = 1 / float(fs)
    t = np.arange(0, N * ts, ts)
    i0 = np.cos(2 * np.pi * t * fc0) * 2 ** 14
    q0 = np.sin(2 * np.pi * t * fc0) * 2 ** 14
    iq0 = i0 + 1j * q0
    sdr.tx([iq0,iq0])  # Send Tx data.

    # Assign frequency bins and "zoom in" to the fc0 signal on those frequency bins
    xf = np.fft.fftfreq(NumSamples, ts)
    xf = np.fft.fftshift(xf)/1e6

programTX(sdr)

def calcTheta(phase):
    # calculates the steering angle for a given phase delta (phase is in deg)
    # steering angle is theta = arcsin(c*deltaphase/(2*pi*f*d)
    arcsin_arg = np.deg2rad(phase)*3E8/(2*np.pi*rx_lo*d)
    arcsin_arg = max(min(1, arcsin_arg), -1)     # arcsin argument must be between 1 and -1, or numpy will throw a warning
    calc_theta = np.rad2deg(np.arcsin(arcsin_arg))
    return calc_theta

def dbfs(raw_data):
    # function to convert IQ samples to FFT plot, scaled in dBFS
    NumSamples = len(raw_data)
    win = np.hamming(NumSamples)
    y = raw_data * win
    s_fft = np.fft.fft(y) / np.sum(win)
    s_shift = np.fft.fftshift(s_fft)
    s_dbfs = 20*np.log10(np.abs(s_shift)/(2**11))     # Pluto is a signed 12 bit ADC, so use 2^11 to convert to dBFS
    return s_shift, s_dbfs

def monopulse_angle(array1, array2):
    ''' Correlate the sum and delta signals  '''
    # Since our signals are closely aligned in time, we can just return the 'valid' case where the signals completley overlap
    # We can do correlation in the time domain (probably faster) or the freq domain
    # In the time domain, it would just be this:
    # sum_delta_correlation = np.correlate(delayed_sum, delayed_delta, 'valid')
    # But I like the freq domain, because then I can focus just on the fc0 signal of interest
    sum_delta_correlation = np.correlate(array1[signal_start:signal_end], array2[signal_start:signal_end], 'valid')
    angle_diff = np.angle(sum_delta_correlation)
    return angle_diff

def scan_for_DOA():
    # go through all the possible phase shifts and find the peak, that will be the DOA (direction of arrival) aka steer_angle
    data = sdr.rx()
    Rx_0=data[0]
    Rx_1=data[1]
    peak_sum = []
    peak_delta = []
    monopulse_phase = []
    delay_phases = np.arange(-180, 180, 2)    # phase delay in degrees
    for phase_delay in delay_phases:   
        delayed_Rx_1 = Rx_1 * np.exp(1j*np.deg2rad(phase_delay+phase_cal))
        delayed_sum = Rx_0 + delayed_Rx_1
        delayed_delta = Rx_0 - delayed_Rx_1
        delayed_sum_fft, delayed_sum_dbfs = dbfs(delayed_sum)
        delayed_delta_fft, delayed_delta_dbfs = dbfs(delayed_delta)
        mono_angle = monopulse_angle(delayed_sum_fft, delayed_delta_fft)
        
        peak_sum.append(np.max(delayed_sum_dbfs))
        peak_delta.append(np.max(delayed_delta_dbfs))
        monopulse_phase.append(np.sign(mono_angle))
        
    peak_dbfs = np.max(peak_sum)
    peak_delay_index = np.where(peak_sum==peak_dbfs)
    peak_delay = delay_phases[peak_delay_index[0][0]]
    steer_angle = int(calcTheta(peak_delay))
    
    return delay_phases, peak_dbfs, peak_delay, steer_angle, peak_sum, peak_delta, monopulse_phase

def Tracking(last_delay):
    # last delay is the peak_delay (in deg) from the last buffer of data collected
    data = sdr.rx()
    Rx_0=data[0]
    Rx_1=data[1]
    delayed_Rx_1 = Rx_1 * np.exp(1j*np.deg2rad(last_delay+phase_cal))
    delayed_sum = Rx_0 + delayed_Rx_1
    delayed_delta = Rx_0 - delayed_Rx_1
    delayed_sum_fft, delayed_sum_dbfs = dbfs(delayed_sum)
    delayed_delta_fft, delayed_delta_dbfs = dbfs(delayed_delta)
    mono_angle = monopulse_angle(delayed_sum_fft, delayed_delta_fft)
    phase_step= 1
    if np.sign(mono_angle) > 0:
        new_delay = last_delay - phase_step
    else:
        new_delay = last_delay + phase_step
    return new_delay

''' Setup Main UI Window '''
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

''' Setup All Windows '''
p1  = ui.setupTrackerGraph(tracking_length)
p2 = ui.setupFirstGraph()
p3 = ui.setupSecondGraph()

''' Collect Data '''
for i in range(20):  
    # let Pluto run for a bit, to do all its calibrations
    data = sdr.rx()
    
#scan once to get the direction of arrival (steer_angle) as the initial point for out monopulse tracker
delay_phases, peak_dbfs, peak_delay, steer_angle, peak_sum, peak_delta, monopulse_phase = scan_for_DOA()
delay = peak_delay  # this will be the starting point if we are doing monopulse tracking
tracking_angles = np.ones(tracking_length)*180
tracking_angles[:-1] = -180   # make a line across the plot when tracking begins

curve1 = p1.plot(tracking_angles)

def update_tracker():
    global tracking_angles, delay
    delay = Tracking(delay)
    tracking_angles = np.append(tracking_angles, calcTheta(delay))
    tracking_angles = tracking_angles[1:]
    curve1.setData(tracking_angles, np.arange(tracking_length))

# Initial Condition
init = False

''' Application Loop '''
def runTracker():
    global ui, init, sdr, tx_gain, rx_gain0, phase_cal

    toggle = ui.getToggle()
    newRX = ui.getRXGain()
    newTX = ui.getTXGain()
    newPhaseCal = ui.getPhaseCal()

    # If toggle is on to continue tracker
    if toggle:
        # If change has occured to Pluto variables
        if init:
            print("Restart Pluto")
            sdr.tx_destroy_buffer()

            sdr = adi.ad9361(uri='ip:192.168.2.1')
            setupPluto(samp_rate, fc0, rx_lo, rx_mode, rx_gain0, rx_gain0, NumSamples, tx_lo, tx_gain)
            # Same as main monopulse initialization
            for i in range(20):  
                data = sdr.rx()
            delay_phases, peak_dbfs, peak_delay, steer_angle, peak_sum, peak_delta, monopulse_phase = scan_for_DOA()
            delay = peak_delay
            tracking_angles = np.ones(tracking_length)*180
            tracking_angles[:-1] = -180
            curve1 = p1.plot(tracking_angles)
            init = False
        update_tracker()
    else:
        # If Rx Dial is changed
        if newRX != rx_gain0:
            rx_gain0 = int(newRX)
            init = True
        
        # If Tx Dial is changed
        # Note: tx_hardwaregain_chan0 does not accept arguments greater than 1. Documentation as to its limits is unclear
        if newTX != tx_gain:
            # tx_gain = int(newTX)
            print("Currently N/A")
            init = True
        
        # If Phase Calibration is changed
        if newPhaseCal != phase_cal:
            phase_cal = newPhaseCal
            init = True
    
timer = pg.QtCore.QTimer()
timer.timeout.connect(runTracker)
timer.start(0)

if __name__ == "__main__":
    sys.exit(app.exec_())

sdr.tx_destroy_buffer()
