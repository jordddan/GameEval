import json

with open("labels.txt","r") as f:
    data = f.readlines()

res = []
for line in data:
    temp = line.strip()
    if len(temp) != 0:
        res.append(temp.split(":")[-1].strip())

with open("labels.json",'w') as f:
    json.dump(res,f)
