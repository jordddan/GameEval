from tofukingdom.agents import ChefAgent,SpyAgent,MaidAgent,GuardAgent,QueenAgent,PrinceAgent,PrincessAgent,MinisterAgent
from tofukingdom.utils.utils import create_message
from chat.gpt3_chat import GPT3
from chat.gpt4_chat import GPT4
import vthread
import json 
import random
import argparse
import os
from tofukingdom.utils.utils import get_model
gpt3 = GPT3()
gpt4 = GPT4()
players = ["Nancy","Tom","Cindy","Jack","Rose","Edward","Robert"]


def init_game(players,prince_model,queen_model,spy_model):
    name2agent = {}
    random.shuffle(players)
    agents = []
    agents.append(PrincessAgent(prince_model,players[0],players))
    agents.append(ChefAgent(prince_model,players[1],players))
    agents.append(SpyAgent(spy_model,players[2],players))
    agents.append(MaidAgent(spy_model,players[3],players))
    agents.append(GuardAgent(queen_model,players[4],players))
    agents.append(QueenAgent(queen_model,players[5],players))
    agents.append(MinisterAgent(queen_model,players[6],players))
    random.shuffle(agents)
    settings = f"PrinceModel: {prince_model.name}\n QueenModel: {queen_model.name} \n SpyModel: {spy_model.name} \n"
    identities = ""
    for agent in agents:
        name2agent[agent.player_name] = agent
        settings += f"Player: {agent.player_name}; LLM: {agent.chatbot.name}; Identity: {agent.role}; \n"
        identities += f"Player {agent.player_name} is the {agent.role};"
    return agents, name2agent, settings, identities

def get_identity_text(agents):
    res = ""
    for agent in agents:
        res += f"{agent.player_name} is the {agent.role}. \n"
    return res

def get_game_result(final_name,i):
    res = {"winner":final_name,"log":f"{i}.log"}
    return res

def update_history(agents_list, temp_message, player_name):
    
    for agent in agents_list:
        if agent.player_name != player_name:
            agent.private_history.append(temp_message)


def game(f,round,prince_model,queen_model,spy_model):

    prince = PrinceAgent(prince_model,players)
    print(f"The {round}-th game begins.\n")

    random.shuffle(players)

    agents_list, name2agent, settings, identities = init_game(players,prince_model,queen_model,spy_model)
    if args.debug:
        print(settings)
        print()
    identities = get_identity_text(agents_list)

    host_speech= "Host: The game now start."
    start_message = create_message("user",host_speech)
    update_history(agents_list,start_message,"host")
    prince.private_history.append(start_message)
    f.write(host_speech + "\n")
    if args.debug:
        print(host_speech)

    for agent in agents_list:
        player_name = agent.player_name

        host_speech= f"Host: The Prince please ask player {player_name} one question."
        host_message = create_message("user",host_speech)
        update_history(agents_list,host_message,"host")
        prince.private_history.append(host_message)
        f.write(host_speech + "\n")
        if args.debug:
            print(host_speech)
        
        # prince ask question 
        question, cot = prince.ask()
        if question is None:
            error = "Question is None."
            print(error)
            return {"error":error}
        temp = f"Prince: {question}"
        temp_message = create_message("user",temp)
        update_history(agents_list,temp_message,"Prince")
        prince_message = create_message("assistant",json.dumps(cot))
        prince.private_history.append(prince_message)
        f.write(temp+"\n")
        f.write(json.dumps(cot)+"\n")
        if args.debug:
            print(temp)
            print(json.dumps(cot))
            print()

        # player answer question 
        answer, cot = agent.chat(identities)
        if answer is None:
            error = "Answer is None."
            print(error)
            return {"error":error}
        temp = f"{player_name}: {answer}"
        temp_message = create_message("user",temp)
        update_history(agents_list,temp_message,player_name)
        private_message = create_message("assistant",json.dumps(cot))
        agent.private_history.append(private_message)
        prince.private_history.append(temp_message)
        f.write(temp+"\n")
        f.write(json.dumps(cot)+"\n")
        if args.debug:
            print(temp)
            print(json.dumps(cot))
            print()

    # choose a player to ask one more question 
    host_speech = f"Host: The Prince please choose a player to ask an extra question."
    host_message = create_message("user",host_speech)
    update_history(agents_list,host_message,"host")
    prince.private_history.append(host_message)
    f.write(host_speech + "\n")
    if args.debug:
            print(host_speech)
            print()

    name, question, cot = prince.ask_choose()
    if name is None:
        error = "Extra name is None."
        print(error)
        return {"error":error}
    temp = f"Prince: I choose {name}, my quesiton is {question}"
    temp_message = create_message("user",temp)
    update_history(agents_list,temp_message,"Prince")
    prince_message = create_message("assistant",json.dumps(cot))
    prince.private_history.append(prince_message)
    f.write(temp+"\n")
    f.write(json.dumps(cot)+"\n")
    if args.debug:
        print(temp)
        print(json.dumps(cot))
        print()

    # player answer an extra question
    answer, cot = agent.chat(identities)
    if answer is None:
        error = "Extra answer is None."
        print(error)
        return {"error":error}
    temp = f"{player_name}: {answer}"
    temp_message = create_message("user",temp)
    update_history(agents_list,temp_message,player_name)
    private_message = create_message("assistant",json.dumps(cot))
    agent.private_history.append(private_message)
    prince.private_history.append(temp_message)
    f.write(temp+"\n")
    f.write(json.dumps(cot)+"\n")
    if args.debug:
        print(temp)
        print(json.dumps(cot))
        print()

    # choose the princess

    host_speech = f"Host: Who do you think is the true princess?"
    host_message = create_message("user",host_speech)
    update_history(agents_list,host_message,"host")
    prince.private_history.append(host_message)
    f.write(host_speech + "\n")
    if args.debug:
        print(host_speech)
        print()

    name, cot = prince.choose()
    if name is None:
        error = "Fianl answer is None."
        print(error)
        return {"error":error}
    if args.debug:
        print(f"The final choice is {name}")
        print(json.dumps(cot))
        print()

    game_result = get_game_result(name2agent[name].role,round)
    if args.debug:
        print(game_result)
    return game_result



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prince_model_name',type=str,default='gpt3')
    parser.add_argument('--spy_model_name',type=str,default='td003')
    parser.add_argument('--queen_model_name',type=str,default='gpt3')
    parser.add_argument('--n',type=int,default='1')
    parser.add_argument('--debug',type=bool,default=True)
    args = parser.parse_args()
    prince_model = get_model(args.prince_model_name)
    spy_model = get_model(args.spy_model_name)
    queen_model = get_model(args.queen_model_name)


    for i in range(args.n):
        log_dir = f"tofukingdom/logs/{args.prince_model_name}_{args.queen_model_name}_{args.spy_model_name}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_name = os.path.join(log_dir,f"{i}.txt")
        with open(file_name,'w') as f:
            game_result = game(f,i,prince_model,queen_model,spy_model)
        if game_result:
            with open("tofukingdom/result.json","a") as f:
                f.write(json.dumps(game_result)+"\n")

            