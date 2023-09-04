from flask import jsonify
import os
import csv
from neo4j import GraphDatabase
import csv
from Old_rels import get_node_name
# from Upload_image import image_upload
from Node_icons import addNode_icon

def upload_csv(request):
    request=request.json
    try:        
        addNode_icon(request['label_name'],request['icon'])
    except Exception as e:
        print("Error in Image : ",e)
    try:
        json_data = request['file_data']
        label=request['label_name']
        if not json_data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        csv_filename = "uploaded_data.csv"
        # Convert JSON to CSV format and save to a file
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(json_data)
        if label=='':
            label = "Node"  # Default label is 'Node'
        response2 = import_csv_to_neo4j(csv_filename, label)
        

        return jsonify({'message': 'CSV data converted and saved successfully in neo4j'},response2), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


BATCH_SIZE = 100000000000000000000000  # Adjust batch size as needed

def import_csv_to_neo4j(csv_path, label):
    uri = "bolt://localhost:7687"  
    username = "alinaqi"      
    password = "12345678"      
    database = 'testingdb'
        
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            column_names = next(reader)  # Read the header line
            # Replace spaces with underscores in header names
            All_char = ['!',"@","#","$","%","^",' ',"&","*","(",")","_","-","=","+","[","{","]","}",";",":","'",'"',",","<",".",">","/","?","\\","|"] 
            for i in range(len(All_char)):
                column_names = [column.replace(All_char[i], "_") for column in column_names]

            with driver.session(database=database) as session:
                query = (
                    f"UNWIND $batch AS row\n"
                    f"MERGE (p:{label} {{"
                )
                for column in column_names:
                    query += f"  {column}: row['{column}'],"
                query = query[:-1]  # Remove the trailing comma
                query += "});"

                rows = []
                for row in reader:
                    row_dict = dict(zip(column_names, row))
                    rows.append(row_dict)
                    if len(rows) == BATCH_SIZE:
                        session.run(query, batch=rows)
                        rows = []
                # Import remaining rows
                if rows:
                    session.run(query, batch=rows)
        return get_node_name(uri,username,password,database,label)
    except Exception as e:
        print('Error is ', e)    
    driver.close()
