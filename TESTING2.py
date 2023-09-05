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
        result1=[]
        print(data)
        for i, a in enumerate(Data):
            query=''
            table = a['table']
            properties = a['property']
            propertyvalue = str(a['propertyvalue'])
            if table=="" and properties==False and propertyvalue=="" and database!="":
                query= f" MATCH (n)  OPTIONAL MATCH (n)-[r]-(relatedNode)   WITH COLLECT(DISTINCT n) AS distinctNodes, COLLECT(DISTINCT relatedNode) AS relatedNodes, r LIMIT {limit} UNWIND r as rel"
                # print("NO 1 is executing")
            elif table!="" and properties!=False and propertyvalue!="" and depth!="":
                query= " match (n:"+f"{table}) "+" optional MATCH (n:"+ f"{table}" + '{'+ f"{properties} :"+ f'"{propertyvalue}"'+"})-"+f"[r*0.."+f"{depth}"+f"]-(relatedNode) "
                query+=" WITH COLLECT(DISTINCT n) AS distinctNodes, COLLECT(DISTINCT relatedNode) AS relatedNodes, r LIMIT {limit} UNWIND r as rel " 
                # print("NO 2 is executing")
            elif table!="" and properties==False and propertyvalue=="":
                query= " match (n:"+f"{table}) "+" OPTIONAL MATCH (n:"+ f"{table}" +")-"+f"[r*0.."+f"{depth}"+"]-"
                query+=f"(relatedNode) WITH COLLECT(DISTINCT n) AS distinctNodes, COLLECT(DISTINCT relatedNode) AS relatedNodes, r LIMIT {limit} UNWIND r as rel"
            returning_query=''' WITH REDUCE(edges = [], rels IN r | 
            edges + [{ source: ID(startNode(rel)) , target: ID(endNode(rel)), type: type(rel) }]
            ) AS allEdges, distinctNodes + relatedNodes AS allNodes
            RETURN { edges: allEdges, nodes: allNodes } AS graphData '''
            query+=returning_query
            print("QUERY IS EXECUTED!!!! ",query)
            with driver.session(database=database) as session:
                result1.append(session.run(query))
            driver.close()
            RES=result1[0]
            for a in RES:
                print(a)
        print("I AM RESULT OF QUERY.......",result1)
        edges,nodes=format_to_edge_node_dict(result1)

    
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
                    formatted_edge = {
                        "source": rel['source'],
                        "target": rel['target'],
                        "type": rel['type']
                    }
                    formatted_result["edges"].append(formatted_edge)
                # print(formatted_result)    
            return formatted_result["edges"],formatted_result['nodes']
        except Exception as e:
            print("ERROR Occured",e)


def remove_duplicate_dicts(data):
    unique_data = []
    seen_data = set()

    for item in data:
        item_json = json.dumps(item, sort_keys=True)

        if item_json not in seen_data:
            seen_data.add(item_json)
            unique_data.append(item)

    return unique_data

