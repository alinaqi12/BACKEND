from neo4j import GraphDatabase
from initialGraph import ini_graph


def get_nodes_and_edges(Data):
    URI = Data['URI']
    driver = GraphDatabase.driver(URI, auth=(Data['username'], Data['password']))
    database = Data['database']
    if Data['node_id']:
        query = f'MATCH (n) where ID(n)={Data["node_id"]} '+"OPTIONAL MATCH (n)-[r]->(relatedNode) WITH collect(DISTINCT n) + collect(DISTINCT relatedNode) AS allNodes, collect(DISTINCT r) AS allRels RETURN { nodes: [node IN allNodes | {id: id(node), label: labels(node)[0], properties: properties(node)}], edges: [rel IN allRels | {source: id(startNode(rel)), target: id(endNode(rel)), type: type(rel)}]} AS graphData;"    
        with driver.session(database=database) as session:
            result = session.run(query).single()["graphData"]
        driver.close()
        return result
    else:
        return "Error Please Define Node ID"
    
def getdata(Request):
    if 'node_id' in Request:
        print(Request)
        nodes_and_edges=get_nodes_and_edges(Request)
    else:
        nodes_and_edges = ini_graph(Request)
        # print(nodes_and_edges)
    
    return nodes_and_edges
