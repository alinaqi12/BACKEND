from flask import Flask, jsonify, request,send_file
from SQL_to_NEO4j import add_data_source
from Get_Nodes import Get_Nodes_Data
from create_relations import get_values
from export import export_data
from runtime_data import get_graph_data_by_query
from Get_Databases import GET_DATABASE
from flask_cors import CORS
import subprocess
import platform
from Nod_Rel import getdata
from CSV import upload_csv
from Json import import_json_data
from existing_node import get_node_labels
from CreateD_BDeleteDB import manage_database
from ShortestPath import shortest_path
from Reltype import get_relationships

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

def start_service(service_name):
    system = platform.system()
    
    if system == "Windows":
        # For Windows, use the 'sc' command to start a service.
        try:
            subprocess.run(["sc", "start", service_name], check=True)
            print(f"Service '{service_name}' started successfully on Windows.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start service '{service_name}' on Windows. Error: {e}")
    
start_service('neo4j')

@app.route('/createrelation', methods=['POST'])
def create_relation():
    if request.method == 'POST':
        data = request.get_json()
        #print(data)
        response=get_values(data)
        print("RESPONSE::::",response)
        return response

@app.route('/getrelations', methods=['GET'])
def getperson():
    if request.method=='GET':
        Data=request.get_json()
        response=Get_Nodes_Data(Data)
        return jsonify(response)

@app.route('/datasource',methods=['POST'])
def datasource():
    if request.method=='POST':
        data=request.get_json()
        print(data)
        response=add_data_source(data['source_url'],data['source_database'],data['source_user'],data['source_password'],data['neo4j_url'],data['neo4j_database'],data['neo4j_user'],data['neo4j_password'],data['keep_relations'])
        return jsonify(response)

@app.route('/exportdata',methods=['POST'])
def exportdata():
    if request.method=='POST':
        data=request.get_json()
        # print(data)
        response=export_data(data)
        return jsonify(response)

@app.route('/getbyquery',methods=['POST'])
def getbyquery():
    if request.method=='POST':
        Data=request.get_json()
        response=get_graph_data_by_query(Data)
        return response
    
@app.route('/getdatabase',methods=['GET'])
def getdatabases():
    if request.method=='GET':
        response=GET_DATABASE()
        return jsonify(response)
    
@app.route('/getdata',methods=['POST'])
def getgraph():
    if request.method=='POST':
        response=getdata(request.get_json())
        return jsonify(response)

@app.route('/get_node_labels',methods=['POST'])
def existing_node():
    if request.method=='POST':
        response=get_node_labels(request)
        return response

@app.route('/manage_database', methods=['POST'])
def manage_database():
    if request.method=='POST':
        response=manage_database(request)
        return jsonify(response)
    
@app.route('/upload_csv_neo', methods=['POST'])
def csv():
    response=upload_csv(request)
    return response 

@app.route('/upload_json_neo', methods=['POST'])
def json():
    response=import_json_data(request)
    return response
    
@app.route('/shortestpath', methods=['POST'])
def get_shortestpath():
    if request.method=="POST":
        reponse=shortest_path(request)
        return jsonify(reponse)

@app.route('/get_available_relationships', methods=['POST'])
def existing_rels():
    if request.method=="POST":
        reponse=get_relationships(request)
        return jsonify(reponse)


if __name__ == '__main__':
    app.run(host="192.168.137.35",debug=True, port=34464)