import json
file_path = "/workspace/qiaodan/tofuking/logs/res.json"


with open(file_path,'r') as f:
    data = f.readlines()

res = {"gpt3":0, "gpt4":0}

for line in data[:100]:
    item = json.loads(line)
    llms = item["llms"]
    score = item["score"]
    for i in range(len(llms)):
        llm = llms[i]
        res[llm] += score[i]

res["gpt3"] /= 4
res["gpt4"] /= 3
print(res)

