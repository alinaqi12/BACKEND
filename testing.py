from neo4j import GraphDatabase
import json

neo4j_uri = 'bolt://localhost:7687'
neo4j_username = 'alinaqi'
neo4j_password = '12345678'
database='testingdb'
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
session = neo4j_driver.session(database=database)

def get_child_nodes(session, node_id):
    query = (
        "MATCH (a)-[*0..1]->(child) "
        f"WHERE ID(a) = {node_id} RETURN child"
    )
    result = session.run(query)

    child_nodes = [record["child"] for record in result]
    return child_nodes

def get_node_and_child_nodes(Data):
    table=Data['Table']
    field=Data['field']
    field_value=Data['field_value']
    query =f"MATCH (a:{table} {{{field}:'{field_value}'}})  "+"RETURN id(a) as nodeID,a"
    #print(query)
    result = session.run(query)
    s= result.single()
    node_id = s['nodeID']
    Parent=s['a']
    #print(Parent)
    #print("Node ID:", node_id)
    try:
        child_nodes =get_child_nodes(session, node_id)
    except :
        print("No child elements! ")
    return Parent, child_nodes

def close():
    session.close()
    neo4j_driver.close()

def convert_to_json(node):

    labels = node.labels
    properties = dict(node)

    json_data = {
        "labels": list(labels),
        "properties": properties
    }

    json_string = json.dumps(json_data, indent=None)

    #print(json_string)
    return json_string
coa=[]

def Get_Data(Data):
    Parent_node,Child_node=get_node_and_child_nodes(Data)
     
    for child in Child_node:
        if child.id!=Parent_node.id:
            res=convert_to_json(child)
            coa.append(res)
    
    # coa_cleaned = [json_string.replace('\n', '') for json_string in res]
    for a in coa:
        print(a)
    Parent_node=convert_to_json(Parent_node)
    print(Parent_node)
#Data={'Table':'Person','field':'CNIC','field_value':'5551879999'}
#Get_Data(Data)