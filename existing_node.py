from flask import Flask, request, jsonify
from neo4j import GraphDatabase


def get_node_labels(request):
    data = request.json

    if "database" in data and "username" in data and "password" in data and "URI" in data:
        try:

            driver_uri = data["URI"]
            driver_user = data["username"]
            driver_password = data["password"]
            database = data["database"]
            global driver
            driver = GraphDatabase.driver(driver_uri, auth=(driver_user, driver_password))

            query = """
            MATCH (n)
            RETURN DISTINCT labels(n) AS node_labels;
            """

            with driver.session(database=database) as session:
                result = session.run(query)

                node_labels = [{"node_labels": record["node_labels"][0]} for record in result]

            return jsonify(node_labels)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid JSON body"}), 400

