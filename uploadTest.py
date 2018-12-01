from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploadr_file():
   if request.method == 'POST':
      f = request.files['file']
      name = "banana.jpg"
      #the name here will have to be changed to something more meaningful
      #f.save(secure_filename(f.filename))
      f.save(name)
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)