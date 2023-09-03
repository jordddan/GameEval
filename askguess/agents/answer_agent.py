import os
import sys
sys.path.append("ask-guess")
from askguess.utils.prompt import get_answerer_role,get_questioner_role
from askguess.utils.utils import create_message,print_messages, convert_messages_to_prompt
class AnswerAgnent:

    def __init__(self, chatbot, object_name, args) -> None:
        
        self.chatbot = chatbot
        self.object_name = object_name
        self.role_easy, self.role_hard = get_answerer_role(object_name)

        self.history = []
        if args.mode == "easy":
            role_message = create_message("system",self.role_easy)
        else:
            role_message = create_message("system",self.role_hard)
        self.history.append(role_message)
 
    def play(self):

        if self.chatbot.name == "td003":
            text_prompt = convert_messages_to_prompt(messages=self.history,role="answerer")
            response = self.chatbot.single_chat(text_prompt)
        else:
            response = self.chatbot.multi_chat(self.history)
        return response
    
    def answer(self):
        # response = self.chatbox.multi_chat(input_list=self.history,role=self.answer_role,role_last = self.role_last)
        # import pdb
        # pdb.set_trace()
        if self.chatbot.name == "td003":
            text_prompt = self.get_answer_prompt()
            response = self.chatbot.single_chat(text_prompt)

        else:
            response = self.chatbot.multi_chat(self.history)

        return response

    def get_answer_prompt(self):
        prompt = "##system##"
        prompt += self.answer_role + "\n"
        flag = (len(self.history) + 1) % 2
        for i in range(len(self.history)):
            if i % 2 == flag:
                prompt += "##questioner##: "
            else: 
                prompt += "##answerer##:"
            prompt += self.history[i]["content"] + "\n\n"
        prompt +=  "##answerer##:"

        return prompt
    
    def get_describe_prompt(self):
        
        prompt = "##system##"
        prompt += self.describe_role + "\n"
        flag = (len(self.history) + 1) % 2
        for i in range(len(self.history)):
            if i % 2 == flag:
                prompt += "##questioner##: "
            else: 
                prompt += "##answerer##:"
            prompt += self.history[i]["content"] + "\n\n"
        prompt += "##answerer##:"

        return prompt
    
    def update_history(self, new_message):
        self.history.append(new_message)


