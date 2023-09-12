from flask import Flask, request, jsonify
from neo4j import GraphDatabase


def get_neighboring_nodes(uri, username, password, node_id, database):
    query = (
        f"MATCH (startNode)-[relationship]-(neighbor) "
        f"WHERE ID(startNode) = {node_id} "
        "RETURN ID(startNode) as source, type(relationship) as type, ID(neighbor) as target, neighbor, labels(neighbor) as neighborLabels"
    )
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            result = session.run(query)
            return [record.data() for record in result]


def expandnode(request):
    print("hereerererer-[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]")
    data = request
    print(data)
    # Extract input data from JSON
    username = data['username']
    password = data['password']
    uri = data['URI']
    database = data["database"]
    node_id = data['node_id']

    # Execute the Cypher query
    results = get_neighboring_nodes(uri, username, password, node_id, database)

    # Create the response structure with "edges" and "nodes"
    response = {"edges": [], "nodes": [],"iconLabels":[]}

    for result in results:
        edge = {
            "source": result["source"],
            "target": result["target"],
            "type": result["type"]
        }
        response["edges"].append(edge)

        node = {
            "id": result["target"],
            "label": result["neighborLabels"][0] if result["neighborLabels"] else "",
            "properties": result["neighbor"]
        }
        response["nodes"].append(node)
    print(response)
    return jsonify(response)
