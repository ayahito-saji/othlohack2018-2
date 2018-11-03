import json

results = []
with open("pn_ja.txt", 'r') as fp:
    for line in fp:
        splitted_line = line.strip().split(":")
        result = {
            "surface": splitted_line[0],
            "surface_read": splitted_line[1],
            "type": splitted_line[2],
            "value": splitted_line[3]
        }
        results.append(result)

with open("pn_ja.json", 'w') as fp:
    json.dump(results, fp, ensure_ascii=False)
