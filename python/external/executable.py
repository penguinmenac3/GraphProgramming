import json
import sys

raw_value = ' '.join(sys.argv[1:])
value = json.loads(raw_value)
result = {}
result["testout"] = value["testin"] / 2
print(json.dumps(result))