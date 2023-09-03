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

def convert_messages_to_prompt(messages,role):
    prompt = ""
    if role == "questioner":
        for message in messages:
            content = message["content"]
            if message["role"] == "user":
                prompt += f"questioner: {content}\n"
            elif message["role"] == "assistant":
                prompt += f"answerer: {content}\n"
            else:
                prompt += f"host: {content}\n"
        prompt += "questioner: "
    else:
        for message in messages:
            content = message["content"]
            if message["role"] == "assistant":
                prompt += f"questioner: {content}\n"
            elif message["role"] == "user":
                prompt += f"answerer: {content}\n"
            else:
                prompt += f"host: {content}\n"
        prompt += "answerer: "
        
    return prompt
