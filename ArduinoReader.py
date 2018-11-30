import serial
import re
import numpy

def arduinoToFloat(ser):
    return float(next(iter(re.findall(r'-?\d+\.?\d*',ser.readline().decode("utf-8"))), 0))
serial.Serial.readable
def getCurrentWeight(ser, samples, tolerance):
    buffer = []
    for i in range(samples):
        buffer.append(ser.readLine())

tolerance = 1
windowMax = 5
window = []
for i in range(windowMax):
    window.append(0)
ser = serial.Serial('COM8', 9600, timeout = 1)

while True:
    if (ser.in_waiting):
        window.pop(0)
        window.append(arduinoToFloat(ser))
        print( numpy.amax(window)-numpy.amin(window))
    #print ("logic")




