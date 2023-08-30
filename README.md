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


## Illusration
Below is a simple demonstration of three designed games: Ask-Guess, SpyFall and TofuKingdom.
<p align=center>
  <img src="assets/GameEval.png?raw=true" width="80%" />
</p>


## Ask-Guess
### Game Introduction
Ask-Guess is a cooperative game involving a questioner and an answerer. At the beginning of the game, the answerer receives a word unknown to the questioner. In each round, the questioner may ask the answerer one question, and the answerer has to answer faithfully. The provided word or phrase must not be included in the answerer’s reply. Both participants should collaborate to minimize the number of Q&A rounds needed for the questioner to deduce the given word or phrase accurately. The questioner should ask targeted questions to progressively narrow down the potential scope of the given word based on the answerer’s responses. The answerer must assess whether the questioner has successfully identified the word and respond with ’Gameover’ to conclude the game.

### Get Started 
**You can direct use the following script to use model `ChatGPT` to play the game.** You can set the word to be guessed in `label_path` and `n` means run n times for each word. The result and the game log will be automatically recorded.
```  
cd ask-guess
python game.py \ 
    --label_path test_labels.json \
    --model_name gpt3 \
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
will be released soon 
## TofuKingdom
will be released soon

## Citing GameEval

```
@article{qiao2023gameeval,
  title={GameEval: Evaluating LLMs on Conversational Games},
  author={Qiao, Dan and Wu, Chenfei and Liang, Yaobo and Li, Juntao and Duan, Nan},
  journal={arXiv preprint arXiv:2308.10032},
  year={2023}
}
```