import json

def addNode_icon(node_label, icon):

    try:
        with open('Node_icons.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []
    new_entry = {"Node": node_label, "iconLabel": icon}
    data.append(new_entry)
    with open('Node_icons.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_node_icon(node_labels):
    # Read the JSON data from the file.
    try:
        with open('Node_icons.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return []

    # Filter the data based on the provided node_labels.
    filtered_data = [entry for entry in data if entry.get("Node") in node_labels]
    return filtered_data

