from spyfall.utils.prompt import game_prompt_en
from spyfall.utils.utils import create_message, print_messages
import json 

class BaseAgent:
    def __init__(self,chatbot,llm_name,player_name,all_players,phrase) -> None:
        self.chatbot = chatbot # llm model
        self.llm_name = llm_name # name of the chatbot e.g. "gpt3" 
        self.game_prompt = game_prompt_en
        self.player_name = player_name # player name 
        self.phrase = phrase
        self.all_players = all_players # the names of all the players
        self.role_prompt = self.get_role_prompt() 

        self.role_messages = self.get_role_messages()
        self.vote_messages = self.get_vote_messages()
        self.private_history = []
        
    def get_role_prompt(self):
        role_prompt = (
            f'''{self.game_prompt}'''
            f'''The players involved in the game are: {json.dumps(self.all_players)}.'''
            f'''You are {self.player_name} \n'''
            f'''Your given phrase is {self.phrase} \n'''  
        )

        return role_prompt


    
    def get_role_messages(self):
        
        messages = []
        messages.append(create_message("system",self.game_prompt))
        temp = f"Now i have read the rules and i know how to play the game, can you offer me some key strategy to win the game? "
        messages.append(create_message("assistant",temp))
        
        temp = f"Sure. At the begining of the game or you are not sure whether you are the spy, you can speak with very general descriptions and use as few words as you can. "
        messages.append(create_message("user",temp))
        temp = f"For example, if your word is 'apple', you can say like 'it's this is a very common object' or 'it's a kind of fruit' "
        messages.append(create_message("user",temp))
        temp = f"You need to analyze the speech of other players carefully to guess what is the common word and what is the spy word."
        messages.append(create_message("user",temp))
        temp = f"If you are sure that you are a spy, you should try to conceal your identity and confuse others not to vote you."
        messages.append(create_message("user",temp))
        temp = f"I understand. "
        messages.append(create_message("assistant",temp))
        temp = f"Now you are {self.player_name}, the word you get is {self.phrase}. You don't know the word of other players. "
        messages.append(create_message("user",temp))
        temp = f"Recieved. "
        messages.append(create_message("assistant",temp))
        
        temp = (
            f'''Your reply should be a string in the json format as follows:\n'''
            '''{"thought":{your though},"speak":{your speak}}\n '''
            f''' "thought" represent your thinking, which can be seen only by your self. \n'''
            f''' "speak" represent your speak in this round, which can been seen by all the other players. \n'''
        )
        messages.append(create_message("user",temp))
        temp = (
            '''Your speak should only contain the few words about the word you received, you should not speak like 'i agree with {player_name}' or other thing irrelevant to the word you received. '''
        )
        messages.append(create_message("user",temp))
        temp = f"I understand.  I will reply with a json string, and i will not repeat other players' speak or my own speak in the previous round. "
        messages.append(create_message("assistant",temp))
        
        return messages
    
    
    def get_vote_messages(self):
        messages = []
        messages.append(create_message("system",self.game_prompt))
        temp = f"Now i have read the rules. But i still need some strategies to better win the game."
        messages.append(create_message("assistant",temp))
        
        temp = f"The voting stage is very important. So i can give some experience in the voting stage. "
        messages.append(create_message("user",temp))
        temp =  f"Great, i will learn from the experience to better win the game. "
        messages.append(create_message("assistant",temp))
        temp =  f"First you should carefully think of the word each players get according to their descriptions. The player whose description is far from the others can be the spy."
        messages.append(create_message("user",temp))
        temp = "You need to constantly guess possible common words and spy words during the game process."
        messages.append(create_message("user",temp))
        temp = f"If you are sure that your word is the spy word, you should think of how to prevent being voted. You should try to confuse other players to hide your identity."
        temp += f"If you think you are not the spy, you should think who might be a spy. And you should encourage other players to vote for the spy in your speech if you have a specific suspicion target to be the spy."
        messages.append(create_message("user",temp))
        temp = f"I understand. "
        messages.append(create_message("assistant",temp))
        
        temp = f"Now you are {self.player_name}, the word you get is {self.phrase}."
        messages.append(create_message("user",temp))
        
        temp = f"Recieved. "
        messages.append(create_message("assistant",temp))
        temp = (
             f'''In the voting stage, your reply should be a string in the json format as follows:\n'''
             '''{"thought":{your though},"speak":{your speak},"name":{voted name}} \n '''
            f''' "thought" represent your thinking, which can be seen only by your self. \n'''
            f''' "speak" represent your speak in the game, which can be seen for all the players. \n'''
            f''' "name" can be only select be the living players. \n '''
        )
        messages.append(create_message("user",temp))
        temp = f"I understand. I will reply with a json string, and i will not repeat other players' speak or my own speak of the previous round. "
        messages.append(create_message("assistant",temp))
        return messages
        
    def describe(self):
        messages = self.role_messages + self.private_history
        messages.append(create_message("system","Remember, you must reply a json string as required. And you must not repeat the statements of other players and your own past statement."))

        if self.chatbot.name == "td003":
            text_prompt = self.convert_messages_to_prompt(messages)
            res = self.chatbot.single_chat(text_prompt)
        else:
            res = self.chatbot.multi_chat(messages)

        try:
            res = json.loads(res)
            though = res["thought"]
            speak = res["speak"]
        except:
            pass

        return speak, res
    
    def vote(self):
        messages = self.vote_messages + self.private_history
        messages.append(create_message("system","Remember, you must reply a json string as required, and the 'speak' must not repeat with the statements of other players or your own past statement. The 'name' must be the same string chosen from the given list 'living players'. "))
        if self.chatbot.name == "td003":
            text_prompt = self.convert_messages_to_prompt(messages)
            res = self.chatbot.single_chat(text_prompt)
        else:
            res = self.chatbot.multi_chat(messages)
        thought = None 
        speak = None 
        name = None
        try:
            res = json.loads(res)
            though = res["thought"]
            speak = res["speak"]
            name = res["name"]
        except:
            pass

        return name, speak, res
        
    def convert_messages_to_prompt(self, messages):
        prompt = ""
        for message in messages:
            if message["role"] == "system":
                prompt +=  "system: "
                prompt += message["content"]
                prompt += "\n"
            elif message["role"] == "assistant":
                prompt += f"{self.player_name}: "
                prompt += message["content"]
                prompt += "\n"
            else:
                prompt += message["content"]
                prompt += "\n"
        prompt += f"{self.player_name}: "
        return prompt