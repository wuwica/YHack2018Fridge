from flask import Flask, render_template, request
from werkzeug import secure_filename

import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

app = Flask(__name__)
from gbcut import gbcutImg

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/ping', methods = ['GET'])
def ping():
   return 'server running'


@app.route('/uploader', methods = ['GET', 'POST'])
def uploadr_file():
   if request.method == 'POST':
      f = request.files['file']
      name = "banana.jpg"
      #the name here will have to be changed to something more meaningful
      #f.save(secure_filename(f.filename))
      f.save(name)
      return 'file uploaded successfully'

@app.route('/')
def test_file():
   return render_template('uploadImg.html')

@app.route('/callgbcut', methods = ['GET', 'POST'])
def gbcutcall():
   if request.method == 'POST':
      f = request.files['file']
      name = request.form['itemname']
      #the name here will have to be changed to something more meaningful
      #f.save(secure_filename(f.filename))
      f.save(name)
      gbcutImg(name)
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)