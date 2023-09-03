from tofukingdom.utils.prompt import game_prompt_en
from tofukingdom.agents.base_agent import BaseAgent

class SpyAgent(BaseAgent):
    def __init__(self,chatbot,name,all_players) -> None:
        super().__init__(chatbot,name,all_players)
        self.role = "Spy"

    def get_role_prompt(self):
        role_prompt = '''
        You now need to play the role of the Spy.
        For the Prince's question, you can choose to say the truth or lie.
        The Maid is your teammate.
        You goal is to mislead the Prince to choose other players except the Princess and the Queen.
        '''
        return role_prompt
