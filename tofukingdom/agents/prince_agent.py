
from tofukingdom.utils.prompt import game_prompt_en
import json
from tofukingdom.utils.utils import create_message,print_messages
class PrinceAgent:
    def __init__(self,chatbot,all_players) -> None:
        self.game_prompt = game_prompt_en
        self.chatbot = chatbot
        self.name = "Prince" 
        self.role_prompt = self.get_role_prompt()
        self.ask_prompt = self.get_ask_prompt()
        self.ask_choose_prompt = self.get_ask_choose_prompt()
        self.choose_prompt = self.get_choose_prompt()

        self.all_players = all_players
        self.private_history = []

    def get_role_prompt(self):
        prompt = (f"You need to play the role of the Prince. \n"
                  f"Your goal is to find the true Princess. \n"
                  "You can ask each player one question. "
                  '''
                   Your question can only be strictly chosen from the three question below: 
                    1. Which player is the Princess?
                    2. What is your identity?
                    3. What is the identity of {player_name} ?
                  '''
                  f"Remember some player could lie to you. "
                  f"So you need to carefully consider each player's response and think whether or not you should trust it. "
                  f"You should not always ask the same question, you should try choosing different questions to verify who is the Princess."
        )
        
        return prompt
    
    def get_ask_prompt(self):
        prompt = (
            f"Your reply must be a JSON string in the following format: \n"
            '''{"thought":{your though},"question":{your question}}\n'''
            f"'thought'  represent your you thinking of which question you want to ask and why. \n"
            f"'question' represent your question.\n"
        )
        return prompt
              
    def get_ask_choose_prompt(self):
        prompt = (
            f"Your reply must be in the json format as below:\n "
            '''{"thought":{your thought},"name":{player_name},"question":{your question}}\n'''
            f"'thought' represent your thinking of which player and which question you should ask to help you find the true Princess. \n"
            f"'name' should be the name of the player you choose to ask. \n"
            f"'question' is the question you want to ask, which should be chosen from the three questions above.\n"
        )
        return prompt
        
    def get_choose_prompt(self):
        prompt = (
            f"Your reply must be a single JSON string without any extra characters in the following format: \n"
            '''{"thought":{your thought},"name":{player_name}}\n'''
            f"'thought' represent you analysis according to your question and the response. \n "
            f"'name' should be the name of the player that you think is the Princess. \n"
            f"'name' must be chosen from names of the players \n"
        )
        return prompt
    
    def ask(self):
        messages = []
        game_message = create_message("system",self.game_prompt)
        messages.append(game_message)
        role_message = create_message("system",self.role_prompt)
        messages.append(role_message)
        messages += self.private_history
        last_message = create_message("system",self.ask_prompt)
        messages.append(last_message)
        cnt = 0
       
        while True:
            try:
                if self.chatbot.name == "td003":
                    prompt = self.convert_messages_to_prompt(messages)
                    res = self.chatbot.single_chat(prompt)
                else:
                    res = self.chatbot.multi_chat(messages)
                res = json.loads(res)
                break
            except:
                cnt += 1
            if cnt >= 3:
                return None, None

        question = res["question"]
        return question, res

    def ask_choose(self):
        messages = []
        first_message = create_message("system",self.role_prompt)
        messages.append(first_message)
        messages += self.private_history
        last_message = create_message("system",self.ask_choose_prompt)
        messages.append(last_message)

        cnt = 0
        while True:
            try:
                if self.chatbot.name == "td003":
                    prompt = self.convert_messages_to_prompt(messages)
                    res = self.chatbot.single_chat(prompt)
                else:
                    res = self.chatbot.multi_chat(messages)
                res = json.loads(res)
                break
            except:
                cnt += 1
            if cnt >= 3:
                return None, None, None

        question = res["question"]
        name = res["name"]
        return name, question, res
    
    def choose(self):
        messages = []
        first_message = create_message("system",self.role_prompt)
        messages.append(first_message)
        messages += self.private_history
        last_message = create_message("system",self.choose_prompt)
        messages.append(last_message)

        cnt = 0
        while True:
            try:
                if self.chatbot.name == "td003":
                    prompt = self.convert_messages_to_prompt(messages)
                    res = self.chatbot.single_chat(prompt)
                else:
                    res = self.chatbot.multi_chat(messages)
                res = json.loads(res)
                break
            except:
                cnt += 1
            if cnt >= 3:
                return None, None
        name = res["name"]
        if name not in self.all_players:
            return None, None
        return name, res
    
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
