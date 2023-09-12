from flask import jsonify
import os
import csv
from neo4j import GraphDatabase
import csv
from Old_rels import get_node_name
# from Upload_image import image_upload
from Node_icons import addNode_icon

def import_json_to_neo4j(json_data, label, username, password, database, uri):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        with driver.session(database=database) as session:
            for data in json_data:
                properties = ", ".join([f"{key}: '{value}'" for key, value in data.items()])
                query = (
                    f"MERGE (n:{label} {{{properties}}})"
                )

                # Execute the query with parameters
                session.run(query)

        return 200
    except Exception as e:
        print("Error:", e)
        return 500
    finally:
        driver.close()

def data_formating(file_data):
    cleaned_data = []
    special_chars = ['!',"@","#","$","%","^",' ',"&","*","(",")","_","-","=","+","[","{","]","}",";",":","'",'"',",","<",".",">","/","?","\\","|"] 

    for data in file_data:
        cleaned_dict = {}
        for key, value in data.items():
            cleaned_key = key
            for char in special_chars:
                cleaned_key = cleaned_key.replace(char, '_')
            cleaned_dict[cleaned_key] = value
        cleaned_data.append(cleaned_dict)

    return cleaned_data


def label_format(string):
    special_chars = ['!', "@", "#", "$", "%", "^", ' ', "&", "*", "(", ")", "_", "-", "=", "+", "[", "{", "]", "}", ";", ":", "'", '"', ",", "<", ".", ">", "/", "?", "\\", "|"]
    for char in special_chars:
        string = string.replace(char, '_')

    # Check if the string starts with a number
    if string and string[0].isdigit():
        # Find the index of the first non-digit character
        index = 0
        while index < len(string) and string[index].isdigit():
            index += 1

        # Extract the leading digits and move them to the end
        digits = string[:index]
        string = string[index:] + digits

    return string


def upload_csv(request):

    try:
        request_data = request.json
        print("wefwfwef")
        #print(request_data)
        if "database" in request_data:
            print(request_data)
            uri = request_data["URI"]
            username = request_data["username"]
            password = request_data["password"]
            database = request_data["database"]
            iconLabel = request_data["icon"]
        else:
            print("in else")
            uri = "bolt://localhost:7687"
            username = "alinaqi"
            password = "12345678"
            database = "testingdb"

        print("hehcehce")
        label = request_data.get("label_name", "Node")  # Default label is 'Node'
        file_data = request_data.get("file_data", [])

        if not file_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        label = label_format(label)

        file_data_formated = data_formating(file_data)
        addNode_icon(label,iconLabel)
        success = import_json_to_neo4j(file_data_formated, label,username,password,database,uri)
        
        

        if success == 200:
            rett = get_node_name(uri,username,password,database,label)
            ret = "JSON data inserted successfully in Neo4j" + rett
            return jsonify({"message": ret}),200
            
        else:
            return jsonify({"error": "Error in Inserting data to Database"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500




