from flask import Flask, request, jsonify
from neo4j import GraphDatabase

def manage_database(request):
    data = request.json
    driver = GraphDatabase.driver(data.get('URI'), auth=(data.get("username"), data.get("password")))
    action = data.get('action')
    database_name = data.get('database')
    
    if action == 'create':
        if create_neo4j_database(database_name,driver):
            return jsonify({"message": f"Database '{database_name}' created successfully!"})
        else:
            return jsonify({"message": f"Failed to create database '{database_name}'."}), 500
    elif action == 'delete':
        if delete_neo4j_database(database_name,driver):
            return jsonify({"message": f"Database '{database_name}' deleted successfully!"})
        else:
            return jsonify({"message": f"Failed to delete database '{database_name}'."}), 500
    else:
        return jsonify({"message": "Invalid action. Use 'create' or 'delete'."}), 400

def create_neo4j_database(database_name,driver):
    try:
        with driver.session() as session:
            query = f"CREATE DATABASE {database_name}"
            session.run(query)
            return True
    except Exception as e:
        print("Error creating database:", str(e))
        return False

def delete_neo4j_database(database_name,driver):
    try:
        with driver.session() as session:
            query = f"DROP DATABASE {database_name}"
            session.run(query)
            return True
    except Exception as e:
        print("Error deleting database:", str(e))
        return False

