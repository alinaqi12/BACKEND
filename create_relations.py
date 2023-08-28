from neo4j import GraphDatabase

# URI = "bolt://localhost:7687"
# AUTH = ("alinaqi", "12345678")
# #database='testingdb'
# driver= GraphDatabase.driver(URI, auth=AUTH)  

def relation(driver,targets,database,single_node=0,add_del='add',relations='multiple'):
    if type(targets) == list:
        targetss = targets
    else:
        targetss = list(targets)
    for a in targetss:
    ################# adding or deleting relation between two specific nodes ##################################
        if single_node==1:
            with driver.session(database=database) as session:
                ################## adding  Relation  between two specific nodes
                if add_del=='add':
                    session.run(
                        f"MATCH (source:{a['source']} {{{a['Source_property']}: '{a['Source_property_value']}'}}) "
                        f"WHERE source.{a['Source_property']} IS NOT NULL "  # Use 'IS NOT NULL' instead of 'exists()'
                        f"MATCH (target:{a['target']}) "
                        f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "
                        f"MERGE (source)-[:{a['relationship']}]->(target) "
                        "RETURN source;")
                ################## Deleting Relation
                if add_del=='del':
                    ################## deleting all relations between two specific nodes 
                    if relations=='multiple':
                        query=(
                            f"MATCH (source:{a['source']} {{{a['Source_property']}: '{a['Source_property_value']}'}}) "
                            f"WHERE source.{a['Source_property']} IS NOT NULL "  # Use 'IS NOT NULL' instead of 'exists()'
                            f"MATCH (target:{a['target']}) "
                            f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "
                            f" (source)-[r]->(target) "
                            " delete r RETURN source;")
                    #################### deleting 1 specific relation between two specific nodes
                    if relations=='single':
                        query=f"MATCH (source:{a['source']} {{{a['Source_property']}: '{a['Source_property_value']}'}}) "+f" WHERE source.{a['Source_property']} IS NOT NULL "+f"MATCH (target:{a['target']}) "+f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "+f" match (source)-[r:{a['relationship']}]->(target) "+" delete r RETURN source;"
                    with driver.session(database=database) as session:
                                    session.run(query)
        
        #################### below we are deleting or adding relation between all nodes      
        else:
            ################## adding relation between all nodes
            if add_del=='add':
                query=f"MATCH (source:{a['source']}) "+f"WHERE source.{a['Source_property']} IS NOT NULL "+f"MATCH (target:{a['target']}) "+f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "+f"MERGE (source)-[:{a['relationship']}]->(target) "+"RETURN source;"
            ################## deleting relation
            if add_del=='del':
                ################## deleting a specific single relation between all nodes 
                if relations=='single':
                    query=f"MATCH (source:{a['source']}) "+f" WHERE source.{a['Source_property']} IS NOT NULL "+f"MATCH (target:{a['target']}) "+f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "+f" match (source)-[r:{a['relationship']}]->(target) "+" delete r RETURN source;"
                ################## deleting all relations between all specific nodes.. means deleting all relations on all nodes but nodes will be chosen on a condition like same CNIC or other identifier 
                if relations=='multiple':
                    query=f"MATCH (source:{a['source']}) "+f" WHERE source.{a['Source_property']} IS NOT NULL "+f"MATCH (target:{a['target']}) "+f"WHERE target.{a['Target_property']} = source.{a['Source_property']} "+f" match (source)-[r]->(target) "+" delete r RETURN source;"                    
            with driver.session(database=database) as session:
                session.run(query)

def get_values(data):
    URI = data['URI']
    AUTH = (data['username'], data['password'])
    #database='testingdb'
    driver= GraphDatabase.driver(URI, auth=AUTH)  


    if data['single_node']!=1:
        Source_property_value=''
        Target_Property_value=''
    else:
        Source_property_value=data['Source_property_value']
        Target_Property_value=data['Target_Property_value']
    targets = [
        {
            'source': data['source'],
            'Source_property': data['Source_property'],
            'Source_property_value': Source_property_value,
            'target': data['target'],
            'Target_property': data['Target_property'],
            'relationship': data['relationship'],
            'Target_property_value':Target_Property_value,
            'database':data['database']
        }
    ]   
    #print(targets)
    relation(driver,targets,data['database'],data['single_node'],data['add_del'],data['relations'])
    return targets

