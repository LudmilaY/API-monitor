import json

json_file = 'metrics.json'

with open(json_file, 'r') as file:
    data = json.load(file)

print(json.dumps(data, indent=4))
