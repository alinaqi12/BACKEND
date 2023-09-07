from flask import jsonify
from neo4j import GraphDatabase
import json

def Graph_Data(data):
    try:
        URI = data['URI']
        driver = GraphDatabase.driver(URI, auth=(data['username'], data['password']))
        database = data['database']
        Data=list(data['Data'])
        depth = data['depth']
        limit = data['limit']
        Graph_Data={}
        result=[]
        for i, a in enumerate(Data):
            query=''
            table = a['table']
            properties = a['property']
            propertyvalue = str(a['propertyvalue'])
            if table=="" and properties==False and propertyvalue=="" and database!="":
                query= f" MATCH (n) WITH DISTINCT n LIMIT {limit} OPTIONAL MATCH (n)-[r]-(relatedNode)  UNWIND r as rel RETURN COLLECT(DISTINCT n) AS nodes, "+"COLLECT({ source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }) AS edges "
                # print("NO 1 is executing")
            elif table!="" and properties!=False and propertyvalue!="" and depth!="":
                query= " match (n:"+f"{table}) with distinct n  LIMIT {limit}"+" optional MATCH (n:"+ f"{table}" + '{'+ f"{properties} :"+ f'"{propertyvalue}"'+"})-"+f"[r*0.."+f"{depth}"+f"]-(relatedNode) "
                query+="UNWIND r as rel RETURN COLLECT(DISTINCT n) AS nodes, "+"COLLECT({ source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }) AS edges " 
                # print("NO 2 is executing")
            elif table!="" and properties==False and propertyvalue=="":
                query= " match (n:"+f"{table}) with distinct n  LIMIT {limit}"+" OPTIONAL MATCH (n:"+ f"{table}" +")-"+f"[r*0.."+f"{depth}"+"]-"
                query+=f"(relatedNode) UNWIND r as rel RETURN COLLECT(DISTINCT n) AS nodes, "+"COLLECT({ source: ID(startNode(rel)), target: ID(endNode(rel)), type: type(rel) }) AS edges "

            print("QUERY IS EXECUTED!!!! ",query)
            with driver.session(database=database) as session:
                result.append(session.run(query).single())
            driver.close()
            # print("I AM RESULT OF QUERY.......",result)

        edges,nodes=format_to_edge_node_dict(result)

    
        Graph_Data={"nodes":nodes,"edges":edges}
        return Graph_Data
        
    except Exception as e:
        return {'error': str(e)}
    
    
def format_to_edge_node_dict(result):
        formatted_result={"nodes":[],"edges":[]}
        if result is None:
            return jsonify({'error': 'No data found'})
        try:
            for result1 in result:
                for node in result1["nodes"]:
                    node_id= node.element_id
                    last_colon_index = node_id.rfind(":")  # Find the last occurrence of ":"

                    if last_colon_index != -1:
                        node_id1 = node_id[last_colon_index + 1:]  # Slice the string after the last ":"
                        
                    # print(node_id1)
                    formatted_node = {
                        "id":node_id1,
                        "label": list(node.labels)[0],  # Assuming a node has only one label
                        "properties": dict(node)
                    }

                    formatted_result["nodes"].append(formatted_node)
                # print(formatted_node)
                # Format relationships
                # print('RESULTS OF EDGES',result1["relationships"])
                for rel in result1["edges"]:
                    # print(rel)
                    formatted_edge = {
                        "source": rel['source'],
                        "target": rel['target'],
                        "type": rel['type']
                    }
                    formatted_result["edges"].append(formatted_edge)
                    # print(formatted_result)
            # print(formatted_result['edges'])                
            # formatted_result["edges"],formatted_result['nodes']
            formatted_result["nodes"]=remove_duplicate_dicts(formatted_result["nodes"])
            formatted_result["edges"]=remove_duplicate_dicts(formatted_result['edges'])
            return formatted_result["edges"],formatted_result["nodes"]
        except Exception as e:
            print("ERROR Occured")


def remove_duplicate_dicts(data):
    unique_data = []
    seen_data = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True)

        if item_json not in seen_data:
            seen_data.add(item_json)
            unique_data.append(item)

    return unique_data

