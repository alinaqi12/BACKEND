from neo4j import GraphDatabase
from initialGraph import ini_graph
from limit import remove_extra_nodes
from Node_icons import get_node_icon
from TESTING2 import Graph_Data

def get_nodes_and_edges(Data):
    URI = Data['URI']
    driver = GraphDatabase.driver(URI, auth=(Data['username'], Data['password']))
    database = Data['database']
    if Data['node_id']:
        query = f'MATCH (n) where ID(n)={Data["node_id"]} '+"OPTIONAL MATCH (n)-[r]-(relatedNode) WITH collect(DISTINCT n) + collect(DISTINCT relatedNode) AS allNodes, collect(DISTINCT r) AS allRels RETURN { nodes: [node IN allNodes | {id: id(node), label: labels(node)[0], properties: properties(node)}], edges: [rel IN allRels | {source: id(startNode(rel)), target: id(endNode(rel)), type: type(rel)}]} AS graphData;"    
        with driver.session(database=database) as session:
            result = session.run(query).single()["graphData"]
        driver.close()
        return result
    else:
        return "Error Please Define Node ID"
    
def getdata(Request):
    try:
        if 'node_id' in Request:
            nodes_and_edges=get_nodes_and_edges(Request)
        else:
            nodes_and_edges = ini_graph(Request)
            # nodes_and_edges = Graph_Data(Request)
            # nodes_and_edges['edges']=[]
            
        # if  'limit' in Request  :
        #     nodes_and_edges=remove_extra_nodes(nodes_and_edges,Request['limit'])    
        
        nodes = nodes_and_edges.get("nodes", [])

        labels = [node.get("label") for node in nodes]
        icons= get_node_icon(list(set(labels)))
        print(icons)
        nodes_and_edges['iconLabels']=icons
        return nodes_and_edges
    except:
        return 'Invalid Request'