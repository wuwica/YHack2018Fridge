import serial
import re
import numpy
from flask import Flask

app = Flask(__name__)
ser = serial.Serial('COM8', 9600, timeout = 1)

def arduinoToFloat(ser):
    return float(next(iter(re.findall(r'-?\d+\.?\d*',ser.readline().decode("utf-8"))), 0))

def getCurrentWeight(ser):
    if (ser.in_waiting):
        return arduinoToFloat(ser)
    else:
        while(not ser.in_waiting):
            continue
            
    return arduinoToFloat(ser)

@app.route('/getWeight',methods=['GET'])
def weightEndpoint():
    return str(getCurrentWeight(ser))
    #print ("logic")
@app.route('/tare', methods=['GET'])
def tareThenGetWeight():
    while (not ser.writable):
        continue
    ser.write(b't')
    return 'ok'





