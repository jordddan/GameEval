import os
import sys
sys.path.append("ask-guess")
from askguess.utils.prompt import get_questioner_role
from askguess.utils.utils import create_message,convert_messages_to_prompt,print_messages

class QuestionAgnent:

    def __init__(self,chatbot, object_name, args) -> None:
        
        self.chatbot = chatbot
        self.object_name = object_name
        self.role_easy, self.role_hard = get_questioner_role()
        self.history = []
        if args.mode == "easy":
            role_message = create_message("system",self.role_easy)
        else:
            role_message = create_message("system",self.role_hard)
        self.history.append(role_message)
    
    def play(self):
        if self.chatbot.name == "td003":
            text_prompt = convert_messages_to_prompt(messages=self.history,role="questioner")
            response = self.chatbot.single_chat(text_prompt)
        else:
            response = self.chatbot.multi_chat(self.history)
        return response
    
    def update_history(self, new_message):
        self.history.append(new_message)



