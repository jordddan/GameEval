import sys
import openai
from func_timeout import func_set_timeout

from utils.config import key_gpt3, api_type_gpt3, api_base_gpt3, api_version_gpt3, engine_gpt3

@func_set_timeout(15)
def get_response(messages):
    response = openai.ChatCompletion.create(
        engine=engine_gpt3,
        temperature=0,
        messages = messages,    
        api_type=api_type_gpt3,
        api_base=api_base_gpt3,
        api_version=api_version_gpt3,
        api_key=key_gpt3,    
        )
    return response

class GPT3:
    def __init__(self) -> None:
        self.name = "gpt3"
    
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
            if cnt >= 5:
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









