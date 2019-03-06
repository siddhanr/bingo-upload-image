import os
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from werkzeug.utils import secure_filename
from predict import get_prediction

UPLOAD_FOLDER	= "image-storage/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg'])
project_id = "happyhackathon" 
model_id = "ICN801453283093139314"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route("/uploader", methods=["POST"])
def upload_image():
    req = request
    filedata = request.files['file'].read()
    file = request.files['file']
    filename = secure_filename(file.filename)
    if file.filename == '':
            return redirect(request.url)
    if file and allowed_file(file.filename):
        res = get_prediction(filedata, project_id, model_id)
        if res.payload[0].classification.score > 0.5:
            response = {"keyword":res.payload[0].display_name}
            return jsonify(response)

    else:
        return "file format has to be jpg"

if __name__ == "__main__":
    app.run()