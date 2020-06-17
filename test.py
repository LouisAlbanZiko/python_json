import json

obj = json.parse(open("data.json", "r").read())
print(json.stringify(obj))