import os
import sys
sys.path.append("ask-guess")
from utils.prompt import get_questioner_role
from utils.utils import create_message,convert_messages_to_prompt,print_messages

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
        if self.chatbot.name == "text003":
            text_prompt = convert_messages_to_prompt(messages=self.history,role="questioner")
            response = self.chatbot.single_chat(text_prompt)
        else:
            response = self.chatbot.multi_chat(self.history)
        return response
    
    def question(self):
        if self.chatbot.name == "text003":
            text_prompt = self.get_question_prompt()
            response = self.chatbot.single_chat(text_prompt)
        else:
            response = self.chatbot.multi_chat(self.history)
        return response

    def get_question_prompt(self):
        
        prompt = "##system##"
        prompt += self.role + "\n"
        flag = (len(self.history) + 1) % 2
        for i in range(len(self.history)):
            if i % 2 == flag:
                prompt += "##questioner##: "
            else: 
                prompt += "##answerer##:"
            prompt += self.history[i]["content"] + "\n\n"
        prompt += "##questioner##:"

        return prompt

    def update_history(self, new_message):
        self.history.append(new_message)



