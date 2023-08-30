import os
import sys

import openai


from func_timeout import func_set_timeout
from utils.config import key_gpt4, api_type_gpt4, api_base_gpt4, api_version_gpt4, engine_gpt4

@func_set_timeout(30)
def get_response(messages):
    response = openai.ChatCompletion.create(
        engine=engine_gpt4,
        temperature=0,
        messages = messages,
        api_type=api_type_gpt4,
        api_base=api_base_gpt4,
        api_version=api_version_gpt4,
        api_key=key_gpt4,
        )
    return response

class GPT4:
    def __init__(self) -> None:
        self.name = "gpt4"
    
    def single_chat(self,content,role=None):
        if role is None:
            role = "You are an AI assistant that helps people find information."
        messages = [
                    {"role":"system","content":role},
                    {"role":"user","content":content}
                    ]
        res = None
        cnt = 0
        
        while True:
            try:
                response = get_response(messages)
                res = response["choices"][0]["message"]["content"]
                break
            except:
                cnt += 1 
            if cnt >= 3:
                break    
        
        return  res

    def multi_chat(self, messages):

        res = None
        cnt = 0
        while True:
            try:
                response = get_response(messages)
                res = response["choices"][0]["message"]["content"]
                break
            except:
                cnt += 1 
            if cnt >= 3:
                break    
        
        return  res
    
if __name__ == "__main__":
    pass









