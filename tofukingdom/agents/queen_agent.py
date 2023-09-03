from tofukingdom.utils.prompt import game_prompt_en
from tofukingdom.agents.base_agent import BaseAgent

class QueenAgent(BaseAgent):
    def __init__(self,chatbot,name,all_players) -> None:
        super().__init__(chatbot,name,all_players)
        self.role = "Queen"

    def get_role_prompt(self):
        role_prompt = '''
        You now need to play the role of the Queen.
        For the Prince's question, you can only speak the lie, you are not allowed to speak the truth.
        The Minister and the Guard is your teammate.
        You goal is to mislead the Prince to choose you as the Princess.
        '''
        return role_prompt
    
