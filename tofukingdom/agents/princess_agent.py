
from tofukingdom.utils.prompt import game_prompt_en
from tofukingdom.agents.base_agent import BaseAgent

class PrincessAgent(BaseAgent):
    def __init__(self,chatbot,name,all_players) -> None:
        super().__init__(chatbot,name,all_players)
        self.role = "Princess"

    def get_role_prompt(self):
        role_prompt = '''
        You now need to play the role of the Princess.
        For the Prince's question, you can only speak the truth.
        The Chef is your teammate.
        You goal is to help the Prince correctly choose the princess.
        '''
        return role_prompt
    
