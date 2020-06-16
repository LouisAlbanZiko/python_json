import json

obj = json.parse('{ "a" : "A", "b" : "B", "list": [ "c", "d" ], "obj": {"one": 1, "two": 2.0, "false": false, "true": true} }')
print(json.stringify(obj))