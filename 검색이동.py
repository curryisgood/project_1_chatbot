from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/이미지검색')
def load_file():
   return render_template('이미지검색.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      a= f.filename
      print(f.save)
      print(a+'.png')
      return 'file uploaded successfully'
      return f

if __name__ == '__main__':
   app.run(debug = True)
