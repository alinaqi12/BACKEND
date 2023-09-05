import re

original_string = "MERGE (n:sabehwaqas {'name': 'sabeeh', 'email': 'sabeeh@gmail.com', 'age': 30})"

# Define a regular expression pattern to match labels in Cypher queries
pattern = r'\([^)]+\):[^{,\s]+'

# Use re.sub() with a lambda function to remove single quotes from matched labels
modified_string = re.sub(pattern, lambda x: x.group().replace("'", ""), original_string)

print(modified_string)
