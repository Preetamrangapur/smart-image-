from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pytesseract
from PIL import Image
import os
import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Uncomment and set this if Tesseract is not detected automatically on Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')  # Serve your frontend HTML here

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

    result = {
        'extracted_text': text,
        'timestamp': datetime.datetime.now().isoformat()
    }
    return jsonify(result)

@app.route('/voice', methods=['POST'])
def voice_input():
    data = request.get_json()
    text = data.get('text', '')

    result = {
        'voice_text': text,
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'received'
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
