from flask import Flask, jsonify,Response, request
from flask_cors import CORS
from Nod_Rel import getdata
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 
    
@app.route('/getdata', methods=['POST'])
def getgraph():
    if request.method == 'POST':
        nodes_and_edges, image_data = getdata(request.get_json())
        # print(nodes_and_edges)
        # Check if there was an error
        if isinstance(nodes_and_edges, str):
            return jsonify({'error': nodes_and_edges})

        # Create a response with JSON data and set the content-type
        response_data = {
            'graph_data': nodes_and_edges,
        }

        # You can also set other headers as needed, such as Access-Control-Allow-Origin
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }

        # Create a Flask response with the image data and set the content-type
        image_response = Response(image_data, content_type='image/jpeg')

        # Combine both responses into one
        response = app.response_class(
            response=json.dumps(response_data),  # Use json.dumps from the json module
            status=200,
            headers=headers,
            mimetype='application/json'
        )

        response.set_data(image_response.get_data())
        response.status_code = 200

        return response   
    


if __name__ == '__main__':
    app.run(host='192.168.137.3',debug=True, port=34464)