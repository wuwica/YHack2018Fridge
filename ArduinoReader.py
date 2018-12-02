import serial
import re
import numpy
import time
import requests
import urllib
from flask import Flask


app = Flask(__name__)
ser = serial.Serial('COM8', 9600, timeout=1000)
time.sleep(3)

def arduinoToFloat(ser):
    return float(next(iter(re.findall(r'-?\d+\.?\d*',ser.readline().decode("utf-8"))), 0))

def getCurrentWeight(ser):
    while(not ser.in_waiting):
        continue
    return arduinoToFloat(ser)
def sendCurrentWeight(ser):
    if (ser.in_waiting):
        weight = str(getCurrentWeight(ser))
        requests.post('https://wuwicajon.wixsite.com/test/_functions-dev/setWeight',
        params=urllib.parse.urlencode({
        'weight': weight,}))

@app.route('/tare', methods=['GET'])
def tareThenGetWeight():
    ser.flush()
    while (not ser.writable):
        continue
    ser.write(b't')

    return 'ok'
if __name__ == '__main__':
   app.run(host='localhost')
print("ASD")
while True:
    sendCurrentWeight(ser)
   # if (not ser.in_waiting):
     #   weight = str(getCurrentWeight(ser))
     #   resp=requests.post('https://wuwicajon.wixsite.com/test/_functions-dev/setWeight',
     #   params=urllib.parse.urlencode({
     #   'weight': weight,}))
     #   print (resp)





