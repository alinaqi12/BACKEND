
from flask import Flask, jsonify, request
from flask_cors import CORS
from Nod_Rel import getdata
import io
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 
    
@app.route('/getdata', methods=['POST'])
def getgraph():
    if request.method == 'POST':
        nodes_and_edges = getdata(request.get_json())
        image_data=open('images/outlook.png', 'rb').read()
        # Check if there was an error
        if isinstance(nodes_and_edges, str):
            return jsonify({'error': nodes_and_edges})

        # Encode the image data as base64
        encoded_image = base64.b64encode(image_data).decode()

        # Create a response JSON object with the image data
        response_data = {
            # 'graph_data': nodes_and_edges,
            'image_data': encoded_image
        }

        return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='192.168.137.3', debug=True, port=34466)
