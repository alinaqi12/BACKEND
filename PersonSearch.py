from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j configuration
uri = "bolt://localhost:7687"  # Change this to your Neo4j database URI
username = "fatima"            # Change this to your Neo4j username
password = "12345678"          # Change this to your Neo4j password
database = 'testing'
# driver = GraphDatabase.driver(uri, auth=(username, password))

def create_driver(uri, username, password):
    return GraphDatabase.driver(uri, auth=(username, password))

@app.route("/search", methods=["POST"])
def search():
    try:
        request_data = request.get_json()
        query = request_data.get("query")
        database = request_data.get("database")
        username = request_data.get("username")
        password = request_data.get("password")
        uri = request_data.get("URI")

        # Validate user input (e.g., check for empty query)
        if not query:
            return jsonify({"error": "Invalid query"}), 400
        
        driver = create_driver(uri, username, password)

        # Execute the Cypher query in Neo4j
        with driver.session(database=database) as session:
            result = session.run(
                f'CALL db.index.fulltext.queryNodes("Person", "{query}") YIELD node, score RETURN node'
            )

            # Process query results into a list of dictionaries
            results_list = [dict(record["node"]) for record in result]

        return jsonify({"results": results_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=34464)
