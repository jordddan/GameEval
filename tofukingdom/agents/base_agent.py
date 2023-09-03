from tofukingdom.utils.prompt import game_prompt_en
from tofukingdom.utils.utils import create_message,print_messages
import json 

class BaseAgent:
    def __init__(self,chatbot,player_name,all_players) -> None:
        self.game_prompt = game_prompt_en
        self.chatbot = chatbot
        self.role = None
        self.role_prompt = self.get_role_prompt()
        self.player_name = player_name 
        self.all_players = all_players
        self.private_history = []

    def get_role_prompt(self):
        role_prompt = '''
        You now need to play the role of the Maid.
        For the Prince's question, you can choose to say the truth or lie.

        '''
        return role_prompt
    
    def chat(self,identities):

        role_prompt = (f"{self.game_prompt} \n"
                f"Now, you are player {self.player_name} "
                f"{self.role_prompt} \n"
                f"This is the identity information of other players: {identities} \n "
                )
        last_prompt = (f'''Your reply must be a JSON string in the following format: \n'''
                '''{"thought":{your thought},"answer":"your answer"} \n'''
                f''' 'thought' represent your thought of how to answer the question according to the rule and your goal. '''
                f''' 'answer' represent your reply to the Prince. ''')
        messages = []
        first_message = create_message("system",role_prompt)
        messages.append(first_message)
        messages += self.private_history
        last_message = create_message("system",last_prompt)
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
            
        answer = res["answer"]
        return answer, res
        
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
