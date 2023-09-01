from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
import os


def upload_image(request,name='NEW_TEST'):
    image_data = request.data
    
    ext='.png'
    
    image = Image.open(BytesIO(image_data))
    image.save(f'images/{name}{ext}')
    
    return 'Image uploaded and processed successfully'


