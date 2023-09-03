from spyfall.agents.base_agent import BaseAgent

from chat.gpt3_chat import GPT3
from chat.gpt4_chat import GPT4
from chat.text003_chat import Text003
from spyfall.utils.utils import create_message, get_model
import argparse
import vthread
import json 
import copy 
import random
import os
# gpt3 = GPT3()
# gpt4 = GPT4()
# text003 = Text003()
# name2model = {"gpt3":gpt3,"gpt4":gpt4,"text003":text003}
players = ["Nancy","Tom","Cindy","Jack","Rose","Edward"]

def init_game(phrase_pair,spy_model, villager_model): 
    # phrase_pair[0]:spy word, phrase_pair[1]:common word
    spy_word = phrase_pair[0]
    villager_word = phrase_pair[1]
    random.shuffle(players) 
    name2agent = {}
    index = random.randint(1,len(players)) # index of the spy 
    spy_name = players[index-1]
    agents_list = []
    for i in range(len(players)):
        
        if i+1 == index:
            phrase = spy_word
            llm = spy_model
            llm_name = llm.name
        else:
            phrase = villager_word
            llm = villager_model
            llm_name = villager_model.name
            
        player_name = players[i]
        agent = BaseAgent(llm,llm_name,player_name,players,phrase)
        name2agent[player_name] = agent
        agents_list.append(agent)
    settings = f'''The spy word is: {spy_word};\n The villager word is {villager_word}.\n'''
    for agent in agents_list:
        settings += f"Player: {agent.player_name}; LLM: {agent.llm_name}; Assigned Word: {agent.phrase} \n"

    return agents_list, spy_name, index, settings

def get_voted_name(name_list):
    counts = {} 

    for string in name_list:
        if string in counts:
            counts[string] += 1
        else:
            counts[string] = 1

    max_count = 0
    most_frequent_string = None
    freq = []
    for string, count in counts.items():
        freq.append(count)
        
        if count > max_count:
            max_count = count
            most_frequent_string = string

    freq.sort()
    return most_frequent_string, freq

def update_history(agents_list:list[BaseAgent], temp_message, player_name, public_messages):
    
    for agent in agents_list:
        if agent.player_name != player_name:
            agent.private_history.append(temp_message)
    public_messages.append(temp_message)

def get_result(agent_list:list[BaseAgent], spy_index, round, i, winer):

    llms = [agent.llm_name  for agent in agent_list]
    players = [agent.player_name for agent in agent_list]

    return {"winer":winer,"players":players,"llms":llms,"spy_index":spy_index,"round":round,"log":f"{i}.log"}
    

def game(f, phrase_pair, spy_model, villager_model, i, args):

    agents_list, spy_name, spy_index, game_settings = init_game(phrase_pair,spy_model,villager_model)
    f.write(game_settings)
    living_players = copy.deepcopy(players)

    # game start 
    PUBLIC_MESSAGES = []
    host_speech= "Host: The game now start."
    start_message = create_message("user",host_speech)
    update_history(agents_list,start_message,"host",PUBLIC_MESSAGES)
    f.write(host_speech + "\n")

    host_speech = f"Host: The living players are:{json.dumps(living_players)}"
    living_player_message = create_message("user",host_speech)
    update_history(agents_list,living_player_message,"host",PUBLIC_MESSAGES)
    f.write(host_speech + "\n")

    if args.debug:
        print(game_settings)
    game_round = 0
    while True:
        game_round += 1
        ## describing
        f.write("---------describing stage-------------")

        host_speech = f"Host: Now it's the describing stage, players have to say something about the received word without directly saying it."
        host_message = create_message("user",host_speech)
        update_history(agents_list,host_message,"host",PUBLIC_MESSAGES)
        f.write(host_speech+"\n\n")

        for agent in agents_list:

            if agent.player_name not in living_players:
                continue
            
            host_speech = f"Host: {agent.player_name}, it's your turn."
            host_message = create_message("user",host_speech)
            update_history(agents_list,host_message,"host",PUBLIC_MESSAGES)
            f.write(host_speech+"\n")

            description, cot = agent.describe()
            
            temp = f"{agent.player_name}: {description}"
            public_message = create_message("user",temp)
            update_history(agents_list,public_message,agent.player_name,PUBLIC_MESSAGES)
            PUBLIC_MESSAGES.append(cot)
            private_message = create_message("assistant",json.dumps(cot))
            agent.private_history.append(private_message)
            f.write(temp+"\n")
            f.write(json.dumps(cot)+"\n\n")

            if args.debug:
                print(cot,agent.phrase)
                print(temp)
                print()

        
        f.write("---------voting stage-------------")

        host_speech = "Host: Now the voting start, please vote for the player you think is the spy and tell the reason why you think he is the spy."
        host_message = create_message("user",host_speech)
        update_history(agents_list,host_message,"host",PUBLIC_MESSAGES)
        f.write(host_speech+"\n")

        name_list = []
        for agent in agents_list:
            
            host_speech = f"Host: {agent.player_name}, it's your turn."
            host_message = create_message("user",host_speech)
            update_history(agents_list,host_message,"host",PUBLIC_MESSAGES)
            f.write(host_speech+"\n")

            if agent.player_name not in living_players:
                continue
            name, speak, cot = agent.vote()
            
            # private message for the player
            private_message = create_message("assistant",json.dumps(cot))
            agent.private_history.append(private_message)

            # public message for the other players
            temp = f"{agent.player_name}: {speak}, i will vote {name} as the spy."
            public_message = create_message("user",temp)
            update_history(agents_list,public_message,agent.player_name,PUBLIC_MESSAGES)
            PUBLIC_MESSAGES.append(cot)

            if args.debug:
                print(cot)
                print(temp)
                print()

            f.write(temp+"\n")
            f.write(json.dumps(cot)+"\n")

            name_list.append(name)

        ## result of this round
        final_name, freq = get_voted_name(name_list)
            
        if final_name not in living_players:
            log_content = "Agent not reture a correct player name."
            print(log_content)
            f.write(log_content+"\n")
            return get_result(agents_list,spy_index,-1,i,"exit"),PUBLIC_MESSAGES
        
        if final_name == spy_name:
            log_content = "the spy loss the game"
            print(log_content)
            f.write(log_content)
            # gameover, spy loss
            return get_result(agents_list,spy_index,game_round,i,"villager"),PUBLIC_MESSAGES
        else:
            ## remove a player
            living_players.remove(final_name)

            host_speech = f"Host: the voting result is {final_name}, he is not the spy. The spy still lives, the game will continue. In the next round, the players' descriptions need to be more specific."
            host_message = create_message("user",host_speech)
            update_history(agents_list,host_message,"host",PUBLIC_MESSAGES)
            f.write(host_speech+"\n\n")

            host_speech = f"Host: Now the living players are:{json.dumps(living_players)}"
            living_player_message = create_message("user",host_speech)
            update_history(agents_list,living_player_message,"host",PUBLIC_MESSAGES)
            f.write(host_speech+"\n\n")

            
        if len(living_players) <= 3:
            log_content = "the spy win the game"
            print(log_content)
            f.write(log_content)
            return get_result(agents_list,spy_index,game_round,i,"spy"),PUBLIC_MESSAGES


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--label_path', type=str, default='spyfall/labels.txt')
    parser.add_argument('--spy_model_name',type=str,default='td003')
    parser.add_argument('--villager_model_name',type=str,default='gpt3')
    parser.add_argument('--n',type=int,default='1')
    parser.add_argument('--debug',type=bool,default=True)
    args = parser.parse_args()
    with open(args.label_path,'r') as f:
        data = f.readlines()

    log_path = f"spyfall/logs/{args.spy_model_name}_{args.villager_model_name}"
    labels = []
    for item in data:
        labels.append(item.strip().split(","))

    for label in labels:
        dir_name = f"{label[0]}&{label[1]}"
        if not os.path.exists(os.path.join(log_path,dir_name)):
            os.makedirs(os.path.join(log_path,dir_name))
    
    spy_model = get_model(args.spy_model_name)
    villager_model = get_model(args.villager_model_name)

    for j in range(args.n):
        for i in range(len(labels)): 
            label = labels[i]
            dir_name = f"{log_path}/{label[0]}&{label[1]}"
            with open(f"{dir_name}/{j}.log",'w') as f:
                res, history = game(f=f,
                                    phrase_pair=label,
                                    spy_model=spy_model,
                                    villager_model=villager_model,
                                    i=j,
                                    args=args)  