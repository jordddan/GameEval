import openai
import sys
from func_timeout import func_set_timeout
from utils.config import  key_td003, api_type_td003, api_base_td003, api_version_td003, engine_td003
import re

import random

@func_set_timeout(30)
def get_response(prompt):

    response = openai.Completion.create(engine=engine_td003,
                            temperature=0,
                            prompt = prompt,
                            max_tokens = 150,
                            api_type = api_type_td003,
                            api_base = api_base_td003,
                            api_version = api_version_td003,
                            api_key=key_td003,
                            )

    return response


def extract_json(string):
    l = string.find("{")
    r = string.find("}") + 1
    json_string = string[l:r]
    
    return json_string
    

class Text003:
    def __init__(self) -> None:
        self.name = "text003"
    
    def single_chat(self,prompt):
        cnt = 0
        res = None 

        # import pdb
        # pdb.set_trace()
        while True:
            try:
                response = get_response(prompt)
                res = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
                index = res.find("##")
                if index != -1:
                    res = res[:index]
                break
            except:
                cnt += 1 
            if cnt >= 3:
                break    
        return res
    
    
if __name__ == "__main__":

    pass









