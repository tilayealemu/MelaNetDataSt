import json
import sys

def encode_geez(filename):
    data = []
    with open(filename) as f:
        for line_num, json_line in enumerate(f):
            spec = json.loads(json_line)
            data.append(spec)

    with open(filename, 'w') as f:
        for line in data:
           print(json.dumps(line, ensure_ascii=False), file=f)