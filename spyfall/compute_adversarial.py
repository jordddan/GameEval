import json
import os

with open("/zecheng/qiaodan/spyfall/labels.txt",'r') as f:
    data = f.readlines()


logs_dir = "/zecheng/qiaodan/spyfall/gpt3_gpt4"
out_path = "/zecheng/qiaodan/spyfall/result/gpt3_gpt4.json"
labels = []
for item in data:
    labels.append(item.strip().split(","))

def compute_adversarial(lines):
    cnt_spy = 0
    cnt_villager = 0
    round_avg = 0
    for line in lines:
        item = json.loads(line)
        winer = item["winer"]
        if winer == "exit":
            continue
        if winer == "spy":
            cnt_spy += 1
        else:
            cnt_villager += 1
        round_avg += item["round"]
    
    round_avg /= cnt_spy + cnt_villager
    
    return {"cnt_spy":cnt_spy,"cnt_villager":cnt_villager,"round_avg":round_avg,"rate":cnt_spy/(cnt_spy + cnt_villager)}
res_dict = {}
for label in labels:
    label_name = f"{label[0]}&{label[1]}"
    dir_name = os.path.join(logs_dir,label_name)
    with open(f"{dir_name}/res.json", 'r') as f:
        lines = f.readlines()
    res = compute_adversarial(lines)
    res_dict[label_name] = res
    
avg = {"round_avg":0,"rate":0} 

for key,value in res_dict.items():
    avg["round_avg"] += value["round_avg"]
    avg["rate"] += value["rate"]

avg["round_avg"] /= len(res_dict) - 1
avg["rate"] /= len(res_dict) - 1
res_dict["avg"] = avg

with open(out_path,'w') as f:
    json.dump(res_dict,f,indent=1)
    