import serial
import re
import numpy
import time
import requests
import urllib
from flask import Flask

app = Flask(__name__)
ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(3)

def arduinoToFloat(ser):
    return float(next(iter(re.findall(r'-?\d+\.?\d*',ser.readline().decode("utf-8"))), 0))

@app.route('/getWeight', methods=['GET'])
def restGet():
    return getCurrentWeight(ser)

def getCurrentWeight(ser):
    while(not ser.in_waiting):
        continue
    return str(arduinoToFloat(ser))

def sendCurrentWeight(ser):
    if (ser.in_waiting):
        weight = str(getCurrentWeight(ser))
        print(weight)
        resp = requests.post('https://wuwicajon.wixsite.com/test/_functions-dev/setWeight?weight=%s' % weight)
        print(resp)
        
@app.route('/tare', methods=['GET'])
def tareThenGetWeight():
    ser.flush()
    while (not ser.writable):
        continue
    ser.write(b't')
    return 'ok'

if __name__ == '__main__':
   app.run(host='localhost')
else:
    while True:
        sendCurrentWeight(ser)





