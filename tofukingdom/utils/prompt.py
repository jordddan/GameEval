game_prompt_en = '''
Here is a game called "Tofu Kingdom".
Translation into English: There is a game called "Tofu Kingdom."

In this game, there are 8 roles of Prince, Princess, Queen, Minister, Chef, Guard, Maid, and Spy.
There is a predetermined Prince.
Other players play one of the remaining roles.

In the game, the Prince doesn't know the identities of the other players.
The Prince needs to guess which player is the Princess.
But the players except the Prince know the identity of each other.
If the Prince correctly chooses the player who is the Princess, both the Chef and the Princess win.
If the Prince chooses a player who is the Queen, then the Queen, Minister, and Guard win.
If the Prince chooses a player who is any other role except the Princess and Queen, then the Maid and Spy win.

During the game, the Prince can ask questions to the other players, the question can only be chosen from the three question below: 
1.Which player is the Princess?
2.What is your identity?
3.What is the identity of {player_name} ?

{player_name} must be chosen from the names of the given players.

For question1, player must answer like: {player_name} is the Princess.
For question2, player must answer like: My identity is {role_name}.
For question3, player must answer like: the identity of {player_name} is {role_name}.

At the end of the game, the Prince can choose a player to ask one more question, and the question options remain the same.
For the Prince's inquiries, the Princess and Chef must tell the truth; the Queen, Minister, and Guard must lie; the Maid and Spy can either tell the truth or lie.
Finally, the Prince should guess who is the Princess according to the questions and answers.
'''


game_prompt_zh = '''
    这有一个叫做 “豆腐王国的游戏”。
    在这个游戏中一共有8个玩家，分别扮演 王子，公主，女王，大臣，厨师，侍卫，女仆，间谍。
    这个游戏中，王子不知道其余玩家的身份，王子需要猜测哪一位玩家是公主。
    如果王子选择的玩家身份是公主，则厨师与公主胜利。
    如果王子选择的玩家身份是女王，则女王，大臣，侍卫胜利。
    如果王子选择的玩家身份是除了公主和女王以外的其他，则女仆和间谍胜利。
    游戏中，王子需要询问每个玩家一个问题，被问的玩家需要给出回答这个问题只能从以下三个问题中选择：
    1.豆腐公主是哪位玩家。
    2.你的身份是什么。
    3.某个玩家的身份是什么。
    问题3的某个玩家可以是除了王子以外的任何一名玩家。
    游戏的最后，王子还可以再次挑选一个玩家询问一次问题，问题依旧只能从上面三个问题中选择。
    对于王子的提问，公主，厨师，必须说真话；女王，大臣，侍卫必须说假话；女仆，间谍可以说真话也可以说假话。
'''