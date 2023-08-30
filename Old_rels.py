from flask import Flask, request, jsonify
from neo4j import GraphDatabase

def get_node_name(uri,username,password,database,node_name):

    try:
        # Function to execute the query and retrieve relationships
        query = f"""
                   MATCH (n:{node_name})-[r]->(relatedNode)
                    RETURN DISTINCT type(r) AS relationship_type, labels(relatedNode)

                """
        print(query)
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            
            with driver.session(database=database) as session:
                
                result = session.run(query, nodeName=node_name)
                result1 = result.data()
                print(result1)
        driver.close()


        relationship_types = []
        related_labels = []
       
        for entry in result1:
            relationship_types.append(entry['relationship_type'])
            related_labels.extend(entry['labels(relatedNode)'])
        #print("node_name: ",node_name)     
        #print("Relationship Types:", relationship_types)
        #print("Related Labels:", related_labels)

        # Execute the MERGE query for each relationship type and related label
        with driver.session(database=database) as session:
            for relationship_type in relationship_types:
                for related_label in related_labels:
                    query = (
                        f"MATCH (startNode:{node_name}), (endNode:{related_label}) "
                        f"MERGE (startNode)-[:{relationship_type}]->(endNode)"
                    )
                    session.run(query)
        # Close the Neo4j driver
        driver.close()
        success_response ={'message': 'Successfully added the old relation to new if exist'}
        return success_response


    except Exception as e:
        error_response = {
            'error': 'An error occurred',
            'details': str(e)
        }
        return error_response

