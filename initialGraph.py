from flask import  request, jsonify
from neo4j import GraphDatabase
import json

def ini_graph(data):
    try:
        URI = data['URI']
        driver = GraphDatabase.driver(URI, auth=(data['username'], data['password']))
        database = data['database']
        table = data['table']
        properties = data['property']
        propertyvalue = str(data['propertyvalue'])
        depth = data['depth']
        limit = data['limit']
        if table=="" and properties==False and propertyvalue=="" and database!="":
            query = "MATCH (n)-[r]->(c) RETURN c "+f"limit {limit}"
        elif table!="" and properties!=False and propertyvalue!="" and depth!="":
            query = "MATCH path=(n:"+ f"{table}" + '{'+ f"{properties} :"+ f'"{propertyvalue}"'+"})-[r*0.."+f"{depth}"+"]-(relatedNode) WITH COLLECT(DISTINCT relatedNode) AS nodes, COLLECT(r) AS allRelationships WITH REDUCE(edges = [], rels IN allRelationships |    edges + [rel in rels |       { source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }     ]) AS edges, nodes RETURN { edges: edges, nodes: nodes } AS graphData;" 
        elif properties==False and propertyvalue=="":
            query = "MATCH path=(n:"+ f"{table}" +")-[r*0.."+f"{depth}"+"]-(relatedNode) WITH COLLECT(DISTINCT relatedNode) AS nodes, COLLECT(r) AS allRelationships WITH REDUCE(edges = [], rels IN allRelationships |    edges + [rel in rels |       { source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }     ]) AS edges, nodes RETURN { edges: edges, nodes: nodes } AS graphData;" 
        else:
            return {'error': "No Query Executed"} 
        with driver.session(database=database) as session:
            result = session.run(query).single()
        driver.close()
        return format_to_edge_node_dict(result)
        
    except Exception as e:
        return {'error': str(e)}
    
    
def format_to_edge_node_dict(result):
        if result is None:
            return jsonify({'error': 'No data found'})

        result_data = result.get("graphData", None)
       
        if result_data is None:
            return jsonify({'error': 'No graph data found in the result'})
        formatted_nodes = []
        for node in result_data.get("nodes", []):
            id= node.element_id
            id= int(id[id.rfind(":") + 1:])
            result_properties = dict(zip(list(node.keys()), list(node.values())))
            formatted_nodes.append({
                "id": id,
                "label": str(list(node.labels)[0]),  # Assuming each node has only one label
                "properties": result_properties
            })

        formatted_edges = []
        for edge in result_data.get("edges", []):
            formatted_edges.append({
                "source": edge["source"],
                "target": edge["target"],
                "type": edge["type"]
            })
        
        # formatted_edges=SetLists(formatted_edges)
        #print("FORMATED: ",formatted_edges)
        # print("--------------")
        formatted_result = {
            "nodes": remove_duplicate_dicts(formatted_nodes),
            "edges": remove_duplicate_dicts(formatted_edges)
        }
        return formatted_result

def remove_duplicate_dicts(data):
    unique_data = []
    seen_data = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True)

        if item_json not in seen_data:
            seen_data.add(item_json)
            unique_data.append(item)

    return unique_data

