from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
import os

filetypes = ('.jpg', '.jpeg', '.png', '.gif')
UPLOAD_FOLDER = 'images'  # Directory to store uploaded images

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in filetypes


def upload_image(request):
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        image_data = file.read()
        name = file.filename.rsplit('.', 1)[0]  # Extract filename without extension
        ext = '.' + file.filename.rsplit('.', 1)[1].lower()

        # Create the images folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        image = Image.open(BytesIO(image_data))
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{name}{ext}'))

        return 'Image uploaded and processed successfully'

    return jsonify({'error': 'Invalid file type'}), 400

