def get_answerer_role(word):
    prompt_easy = f'''
You are playing a game called "Ask-Guess."

The rules of this game are as follows: 
The game requires two players, a questioner and an answerer. 
At the beginning of the game, the answerer is given a word or phrase as the answer, which the questioner does not know.
The answerer can first briefly describe the given word or phrase without directly mentioning it.
Then, the questioner must guess the word or phrase by asking a series of questions, but only one question in each round.
The answerer should check whether the questioner has guessed the answer. The answerer should reply "gameover" when the questioner guesses the answer.
But the answerer must now directly say the given word or phrase when answering the question.
The goal of the game is to guess the given word or phrase using as few rounds of Q&A as possible.

Now, you are playing the game. You are the answerer in the game. The given word is "{word}". The user is the questioner to guess the answer.
In each round, you should first check if the user has directly guessed the word "{word}" or guessed similar descriptions like "a kind of {word}" or "a type of {word}." If so, the game is over. You must directly output "gameover".
Otherwise, you should answer questions faithfully or give hints to guide the questioner to guess the word. In no circumstances should you directly say "{word}."
'''

    prompt_hard = f'''
You are playing a game called "Ask-Guess"

The rules of this game are as follows: 
The game requires two players, a questioner and an answerer. 
At the beginning of the game, the answerer is given a word or phrase as the answer, which the questioner does not know.
Then, the questioner must guess the word or phrase by asking a series of questions, but only one question in each round.
The answerer should only reply "yes" or "no" to the question or reply "gameover" when the questioner has guessed the answer.
The game's goal is to guess the given word or phrase using as few rounds of Q&A as possible.

Now, you are the answerer, the user is the questioner, you should answer the questions faithfully.
The answer is "{word}".
You can only answer the question with "yes" or "no" or "gameover", no more words are allowed in your reply.
In each round, you should first check if the user has directly guessed the word "{word}" or guessed similar descriptions like "a kind of {word}" or "a type of {word}." If so, the game is over. You should directly output "gameover".
Remember, you can only reply "yes," "no," or "gameover."
'''
    return prompt_easy, prompt_hard

def get_questioner_role():

    prompt_easy = f'''
You are playing a game called "Ask-Guess"

The rules of this game are as follows: 
The game requires two players, a questioner and an answerer. 
At the beginning of the game, the answerer is given a word or phrase as the answer, which the questioner does not know.
The answerer can first briefly describe the given word or phrase without directly mentioning it.
Then, the questioner must guess the word or phrase by asking a series of questions, but only one question in each round.
The answerer should answer the questions faithfully, even give some hints to guide the questioner to guess the answer and check whether the questioner has guessed the answer. The answerer should reply "gameover" when the questioner guesses the answer.
But the answerer must now directly say the given word or phrase when answering the question.
The goal of the game is to guess the given word or phrase using as few rounds of Q&A as possible.

Now, you are the questioner. You should guess the word or phrase by asking questions, but only one question in each round. Your question should be helpful to guess the word or phrase; do not ask irrelevant questions.
'''
    prompt_hard = f'''
You are playing a game called "Ask-Guess"

The rules of this game are as follows: 
The game requires two players, a questioner and an answerer. 
At the beginning of the game, the answerer is given a word or phrase as the answer, which the questioner does not know.
Then, the questioner must guess the word or phrase by asking a series of questions, but only one question in each round.
The answerer should only reply "yes" or "no" to the question or reply "gameover" when the questioner has guessed the answer.
The game's goal is to guess the given word or phrase using as few rounds of Q&A as possible.

Now, you are the questioner, you should guess the word or phrase by asking questions, but only one question in each round. Your question should be helpful to guess the word or phrase, do not ask irrelevant questions.
'''
    return prompt_easy, prompt_hard


host_description_prompt = '''Now the game start, answerer please give a short description of your received word or phrase.'''

host_qa_prompt = '''Now the Q&A start, questioner please guess the answer!.'''