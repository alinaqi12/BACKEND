from flask import Flask
from flask import jsonify
from flask import request
from neo4j import GraphDatabase

app = Flask(__name__)

# Define a function to query Neo4j and retrieve the first-depth nodes and relationships
def get_first_depth_nodes_with_relationships(node_id, database, uri, username, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        query = (
            "MATCH path = (startNode)-[rel *1]-(endNode) "
            f"WHERE ID(startNode) = {node_id} "
            "UNWIND nodes(path) as node "
            "RETURN ID(node) as id, labels(node) as labels, relationships(path) as rel"
        )
        print(query)
        with driver.session(database=database) as session:
            result = session.run(query)
    
        first_depth_data = []
        for record in result:
            node_data = record["node"]
            rel_data = record["rel"]
            
            first_depth_data.append({
                "id": node_data["id"],
                "labels": node_data["labels"],
                "relationship": dict(rel_data)
            })

        return first_depth_data

    except Exception as e:
        print("Error:", str(e))
        return []

# Define a Flask route to get first-depth nodes with relationships
@app.route('/expand', methods=['POST'])
def api_get_first_depth_nodes_with_relationships():
    try:
        data = request.get_json()
        database = data.get('database')
        node_id = data.get("node_id")
        uri = data.get('URI')
        username = data.get("username")
        password = data.get("password")

        if not node_id:
            return jsonify({"error": "Missing 'node_id' in the request body"}), 400

        first_depth_data = get_first_depth_nodes_with_relationships(
            node_id, database, uri, username, password
        )

        response_data = first_depth_data

        return jsonify({"first_depth_data": response_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="192.168.18.84", debug=True, port=34465)
