#!/usr/bin/env python

# small python script to watch the CTS line of a serial interface

import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
ser.setRTS(False)
ser.setDTR(False)

oldcts = None
while True:
	cts = ser.getCTS()
	if cts != oldcts:
		print time.time(), "CTS: ", cts
		oldcts = cts
	time.sleep(0.5)

ser.close()
