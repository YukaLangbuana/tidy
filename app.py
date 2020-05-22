import json
import pandas as pd
import os
from werkzeug.utils import secure_filename
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response, request, send_file

app = Flask(__name__, static_folder="static", static_url_path='')


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=["POST"])
def upload():
    if "file" in request.files:
        request.files['file'].save(secure_filename(request.files['file'].filename))
        return jsonify(message='File Uploaded'), 200
    else:
        return jsonify(message='Something happened'), 500

@app.route('/process/<filename>', methods=["POST"])
def process(filename):
    filename = _cleanup(filename)
    return jsonify(file_name=filename), 200

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

def _cleanup(file):
    converted_filename = (file).split('.')[0]+'-converted.xls'
    df1 = pd.read_excel(file)
    df2 = []
    for item in df1['good_description']:
        df2.append(json.loads(item))
    df2 = pd.DataFrame(df2)
    # df3 = pd.merge(df1, df2, left_index=True, right_index=True)
    writer = pd.ExcelWriter(converted_filename)
    df2.to_excel(writer)
    writer.save()
    return converted_filename
