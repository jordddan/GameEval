from chat.gpt3_chat import GPT3
from chat.gpt4_chat import GPT4
from chat.text003_chat import Text003

def get_model(model_name):
    model = None
    if model_name == "gpt3":
        model = GPT3()
    if model_name == "gpt4":
        model = GPT4()
    if model_name == "td003":
        model = Text003()
    return model

def create_message(role,content):
    return {"role":role,"content":content}

def print_messages(messages):
    for message in messages:
        print(message)

