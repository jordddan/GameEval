import json 

from agents.answer_agent import AnswerAgnent
from agents.question_agent import QuestionAgnent
from utils.utils import get_model, create_message
from utils.prompt import host_description_prompt, host_qa_prompt
import argparse
import json 



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name',type=str,default='gpt3')
    parser.add_argument('--label_path',type=str,default="labels.json")
    parser.add_argument('--mode',type=str,default='easy')
    parser.add_argument('--n',type=int,default='20')
    args = parser.parse_args() 

    model_name = args.model_name
    mode = args.mode
    N = args.n


    file_path = f"guess_result_{mode}_{model_name}.json"
    output_path = f"avg_result_{mode}_{model_name}.json"
    with open(file_path,'r') as f:
        data = f.readlines()

    res = {}

    # error_type: EndingError, AnswerMentionedError, RoundLimitError, ChatError, SuccessfulTrial
    for item in data:
        line = json.loads(item)
        name = line["object"].replace(" ","_")
        error_type = line["error_type"]
        round = line["round"]
        if name not in res:
            res[name] = {"round":0,"EndingError":0,"SuccessfulTrial":0,"ChatError":0,"RoundLimitError":0,"AnswerMentionedError":0}
        if name in res:
            res[name][error_type] += 1
            if round > 0:
                res[name]["round"] += round

    for key,value in res.items():
        if res[key]["SuccessfulTrial"] != 0:
            res[key]["round"] /= res[key]["SuccessfulTrial"]
        else:
            res[key]["round"] = 30


    data = res

    # error_type: EndingError, AnswerMentionedError, RoundLimitError, ChatError, SuccessfulTrial

    acc_avg = { "round": 0,
    "EndingError": 0,
    "ChatError": 0,
    "SuccessfulTrial": 0,
    "RoundLimitError": 0,
    "AnswerMentionedError": 0}

    cnt_correct = 0
    for name,item in data.items():
        if item["round"] != 0:
            cnt_correct += 1
        for key in item:
            acc_avg[key] += item[key]

    for key in acc_avg:
        if key == "round":
            acc_avg[key] /= cnt_correct
        else:
            acc_avg[key] /= len(data) * N

    data["avg"] = acc_avg

    with open(output_path,'w') as f:
        json.dump(data,f,indent=1)