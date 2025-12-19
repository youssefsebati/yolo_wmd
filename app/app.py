from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import cv2
import numpy as np
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = YOLO("yolov8n.pt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier uploadé"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Fichier vide"}), 400

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    results = model(img)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"result_{filename}")
    results[0].save(output_path)

    return jsonify({
        "original": f"/uploads/{filename}",
        "result": f"/uploads/result_{filename}"
    })

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
