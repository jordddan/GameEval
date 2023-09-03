# GameEval: GameEval: Evaluating LLMs on Conversational Games

[[`Paper`](https://arxiv.org/pdf/2308.10032v1.pdf)]  [[`BibTeX`](#citing-gameeval)]

GameEval try to evalutate powerful LLMs by playing conversational games.GameEval treats
LLMs as game players and assigns them distinct roles with
specific goals achieved by launching conversations of various forms, including discussion, question answering, and voting. 

## Involved Capabilities
GameEval is distinct from other evaluation methods, as it requires not only the model’s common capabilities like instruct-following but also the model’s higher-level skills, including cooperative&adversarial strategies, and even deceptive strategies and long-term planning. In this section, we introduce various distinctive capabilities that can be effectively evaluated by conversational games. We show shows the
capabilities of LLMs that can be examined by these games.
| Capabilities         	| Ask-Guess 	| SpyFall 	| TofuKingdom 	|
|----------------------	|-----------	|---------	|-------------	|
| Cooperative Strategy 	| ✓         	| ✓       	| ✓           	|
| Adversarial Strategy 	| X         	| ✓       	| ✓           	|
| Specific Knowledge   	| ✓         	| ✓       	| X           	|
| Multi-hop Reasoning  	| ✓         	| ✓       	| ✓           	|
| Deceptive Strategy   	| X         	| ✓       	| ✓           	|
| Long-term Planning   	| ✓         	| ✓       	| X           	|
| Instruct-Following   	| ✓         	| ✓       	| ✓           	|
||||

## Expiremental Result of the Original Version

**Experimental results on GameEval clearly demonstrate high discrimination in the capabilities of models under evaluation.**
<p align=center>
  <img src="assets/res.png?raw=true" width="50%" />
</p>

### Ask-Guess
The reult of the easy version. (with prior description from the answerer)
| Model | Round | ST | EE | RLE | AME | CE |
|---|---|---|---|---|---|---|
| TD003 | 4.39 | 82.71 | 9.47 | 1.84 | 5.97 | 0.01 |
| ChatGPT | 6.01 | 53.39 | 8.13 | 14.63 | 23.21 | 0.64 |
| GPT4 | 1.57 | 97.69 | 0.80 | 1.01 | 0.47 | 0.03 |

The reult of the hard version. (without prior description from the answerer)

| Model   	| Round 	| ST    	| EE    	| RLE   	| AME  	| CE   	|
|---------	|-------	|-------	|-------	|-------	|------	|------	|
| TD003   	| 15.13 	| 42.36 	| 19.18 	| 37.19 	| 0.36 	| 0.91 	|
| ChatGPT 	| 13.78 	| 40.50 	| 3.88  	| 49.89 	| 4.57 	| 1.16 	|
| GPT4    	| 4.01  	| 92.77 	| 2.95  	| 0.84  	| 2.75 	| 0.69 	|

### SpyFall
S-model means the model plays the spy, V-model means the model plays the villagers.
<p align=center>
  <img src="assets/res1.png?raw=true" width="40%" />
  <img src="assets/res2.png?raw=true" width="40%" />
</p>

### TofuKingdom
We let different LLMs play all the roles in the same camps to perform a adversarial game. The model that represent a winning camp can get one point. 

| Prince  	| Spy     	| Queen   	| ChatGPT 	| GPT4 	| TD003 	|
|---------	|---------	|---------	|---------	|------	|-------	|
| TD003   	| GPT4    	| ChatGPT 	| 7       	| 9    	| 4     	|
| TD003   	| ChatGPT 	| GPT4    	| 5       	| 11   	| 4     	|
| ChatGPT 	| GPT4    	| TD003   	| 8       	| 7    	| 5     	|
| ChatGPT 	| TD003   	| GPT4    	| 5       	| 9    	| 6     	|
| GPT4    	| TD003   	| ChatGPT 	| 6       	| 7    	| 7     	|
| GPT4    	| ChatGPT 	| TD003   	| 8       	| 8    	| 4     	|
| -       	| -       	| Total   	| 39      	| 51   	| 30    	|
|

## Illustration
Below is a simple demonstration of three designed games: Ask-Guess, SpyFall and TofuKingdom.
<p align=center>
  <img src="assets/GameEval.png?raw=true" width="80%" />
</p>


## How to use GameEval

### For Azure OpenAI
You can create a `chat/config.py` file with reference to the `chat/config_example.py` file, and fill in your Azure OpenAI account information.

### For other LLMs
For other models including Official OpenAI models and open-source models, you can create a chat file in folder `chat` to create a chatbot which receive messsages or text prompt as input and give the response as output.
You can read other files in folder `chat` for reference.

### Install Packages
```
pip install openai
pip install vthread
pip intsall func_timeout
```

## Ask-Guess
### Game Introduction
Ask-Guess is a cooperative game involving a questioner and an answerer. At the beginning of the game, the answerer receives a word unknown to the questioner. In each round, the questioner may ask the answerer one question, and the answerer has to answer faithfully. The provided word or phrase must not be included in the answerer’s reply. Both participants should collaborate to minimize the number of Q&A rounds needed for the questioner to deduce the given word or phrase accurately. The questioner should ask targeted questions to progressively narrow down the potential scope of the given word based on the answerer’s responses. The answerer must assess whether the questioner has successfully identified the word and respond with ’Gameover’ to conclude the game.

### Get Started 
**You can direct use the following script to use model `ChatGPT` to play the game.** You can set the word to be guessed in `label_path` and `n` means run n times for each word. The result and the game log will be automatically recorded.
```  
cd ask-guess
python game_askguess.py \ 
    --label_path test_labels.json \
    --model_name gpt3 \
    --mode easy \
    --debug false \
    --n 30
```
**When all the game is over, you can compute the average result mentioned in the paper by run the file `compute.py`.**

### Case
To better understand how conversational games reflect the gap in model capabilities, we show the game dialogue in Ask-Guess without prior description.
<p align=center>
  <img src="assets/case1.png?raw=true" width="100%" />
</p>
As we can see, both ChatGPT and GPT-4 can correctly understand the tasks, and they ask and answer questions according to the game rules.
However, for a given goal, GPT-4 has demonstrated an astonishing planning ability; the series of questions it asks follow a specific taxonomy. In each round, GPT-4 shows a clear awareness of the impossible objectives that have been ruled out by previous Q\&A and ask new questions targeted at the remaining part. However, the questions ChatGPT asks seem more disorganized and disoriented.


## SpyFall

### Game Introduction 
This game has six players, including one spy and five villagers.
At the beginning of the game, everyone will receive a word.
The spy will receive the spy word, and others will receive the common word.
Spy word is different but relevant to the common word. For example, the spy word can be "lion," and the common word is "tiger."
There are two stages in each round of the game.
In the first stage, everyone needs to describe the word he got but cannot say the given word directly.
In the second stage, everyone should vote for a player he thinks is the spy according to the descriptions in the first stage and state why he thinks this player is a spy.

### Get Started 

```
cd spyfall
python game_spyfall.py \ 
    --label_path spyfall/labels.txt \
    --spy_model_name gpt3 \
    --villager_model_name gpt3 \
    --debug false \
    --n 30
```

## TofuKingdom

### Game Introduction
This game is a role-playing text reasoning game.
It has eight roles, including Prince, Princess, Queen, Minister, Chef, Guard, Maid, and Spy.
The players, except the Prince, know the real identity of the rest of the players.
The Prince needs to guess which player is the Princess by asking one question to each player.
During the game, the Prince's question can only be chosen from the three questions below: 
1. Who is the Princess;
2. What is your identity;
3. What is the identity of \{player\_name\}.

There are three different camps in this game.
The Princess and Chef belong to the Prince Camp; they must tell the truth when answering the question.
The Queen, Minister, and Guard belong to the Queen Camp; they must tell a lie when answering the question.
The Spy and the Maid belong to the Spy Camp and can choose to speak the truth or lie.
After asking each player one question, the Prince can still choose one player to ask an extra question.
The question should also be chosen from one of the three questions mentioned above.
Then the Prince has to choose a player who he thinks is the Princess.
If the Prince correctly chooses Princess, the Chef and the Princess win.
If the Prince chooses the Queen, the Queen, Minister, and Guard win.
If the Prince chooses a player whose identity is neither the Princess nor the Queen, the Maid and Spy wins. 

### Get Started
```
cd spyfall
python game_spyfall.py \ 
    --prince_model_name gpt3 \
    --queen_model_name gpt4 \
    --spy_model_name td003 \
    --debug false \
    --n 20  
```


## Citing GameEval

```
@article{qiao2023gameeval,
  title={GameEval: Evaluating LLMs on Conversational Games},
  author={Qiao, Dan and Wu, Chenfei and Liang, Yaobo and Li, Juntao and Duan, Nan},
  journal={arXiv preprint arXiv:2308.10032},
  year={2023}
}
```