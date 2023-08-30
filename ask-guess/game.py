import json

from agents.answer_agent import AnswerAgnent
from agents.question_agent import QuestionAgnent
import vthread
import logging
import os
import re
from utils.utils import get_model, create_message
from utils.prompt import host_description_prompt, host_qa_prompt
import argparse
import json 

def checkin(word, text):
    '''
        check whether the answerer directly use the word as hint
    '''
    pattern = r'[^\w\s]'
    
    replaced_text = re.sub(pattern, ' ', text)
    
    if (" " + word + " ") in replaced_text:
        return True

    return False

def game(object, f, model, args):
    word = object.replace("_"," ")
    flag = False # True meas a successful trial, False means an error happened.
    cnt = 0  # to record the game round
    answer_agent = AnswerAgnent(model, word, args)
    question_agent = QuestionAgnent(model, word, args)
    error_type = None
    while True:
        # ---------- Describing Stage ----------
        if args.mode == "easy" and cnt == 0:
            # host describing prompt
            host_message = create_message("system",host_description_prompt)
            answer_agent.update_history(host_message)
            question_agent.update_history(host_message)

            description = answer_agent.play()
            f.write(f"description: {description}"+"\n")

            if description == None:
                error_type = "ChatError"
                break
            if checkin(word.lower(), description.lower()):
                error_type = "AnswerMentionedError"
                break

            questioner_message = create_message("user",description)
            answerer_messsage = create_message("assistant",description)
            answer_agent.update_history(answerer_messsage)
            question_agent.update_history(questioner_message)
            # import pdb
            # pdb.set_trace()
            if args.debug:
                print(f"description: {description}"+"\n")
            f.write(f"description: {description}"+"\n")
            cnt += 1 
            continue

        # ---------- Q&A Stage ----------

        # host Q&A prompt
        host_message = create_message("system",host_qa_prompt)
        answer_agent.update_history(host_message)
        question_agent.update_history(host_message)

        question = question_agent.play()

        if question == None:
            error_type = "ChatError"
            break
        questioner_message = create_message("assistant",question)
        answerer_messsage = create_message("user",question)
        answer_agent.update_history(answerer_messsage)
        question_agent.update_history(questioner_message) 
        if args.debug:
            print(f"question: {question}"+"\n")
        f.write(f"question: {question}"+"\n")

        answer = answer_agent.play()
        if answer == None:
            error_type = "ChatError"
            break
        questioner_message = create_message("user",answer)
        answerer_messsage = create_message("assistant",answer)
        answer_agent.update_history(answerer_messsage)
        question_agent.update_history(questioner_message) 
        if args.debug:
            print(f"answer: {answer}"+"\n")
        f.write(f"answer: {answer}"+"\n")
        cnt += 1 

        # ---------- Check the Result ----------
        if "gameover" in answer.lower() or "game over" in answer.lower():
            if word.lower() in question.lower():
                flag = True
                break
            else:
                # wrongly end the game 
                error_type = "EndingError"
                break

        # break the rule
        if checkin(word.lower(), answer.lower()):
            error_type = "AnswerMentionedError"
            break
        if cnt > 30:
            error_type = "RoundLimitError"
            break

    if flag:
        if args.debug:
            print({"object":word,"round":cnt-1,"error_type":"SuccessfulTrial"})
        return {"object":word,"round":cnt-1,"error_type":"SuccessfulTrial"}
    else:
        if args.debug:
            print({"object":word,"round":-1,"error_type":error_type})
        return {"object":word,"round":-1,"error_type":error_type}


@vthread.pool(20)
def run(word,i,model,args):
    with open(f"logs_easy_{args.model_name}/{word}/{i}.log","w") as f:
        res = game(word,f,model,args)
        res["log"] = f"{i}.log"
    with open(f"guess_result_easy_{args.model_name}.json","a") as f: 
        f.write(json.dumps(res)+"\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--label_path', type=str, default='labels.json')
    parser.add_argument('--model_name',type=str,default='gpt3')
    parser.add_argument('--mode',type=str,default='easy')
    parser.add_argument('--n',type=int,default='20')
    parser.add_argument('--debug',type=bool,default=False)
    args = parser.parse_args()
    model = get_model(args.model_name)
    with open(args.label_path,'r') as f:
        labels = json.load(f)

    ## prepare log folder
    for label in labels:
        log_dir = f"logs_easy_{args.model_name}/{label}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    ## run multiple times for each word
    for i in range(0,len(labels)):
        label = labels[i]
        for i in range(args.n):
            run(label,i,model,args)

    vthread.pool.wait() 

