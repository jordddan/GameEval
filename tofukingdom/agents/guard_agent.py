
from tofukingdom.utils.prompt import game_prompt_en
from tofukingdom.agents.base_agent import BaseAgent
class GuardAgent(BaseAgent):
    def __init__(self,chatbot,name,all_players) -> None:
        super().__init__(chatbot,name,all_players)
        self.role = "Guard"

    def get_role_prompt(self):
        role_prompt = '''
        You now need to play the role of the Guard.
        For the Prince's question, you can only speak the lie, you are not allowed to speak the truth.
        The Queen and the Minister is your teammate.
        You goal is to mislead the Prince to choose the Queen as the Princess.
        '''
        return role_prompt
