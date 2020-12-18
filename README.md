# Reversi Game Project
### Team members
-----
- Team leader:
	- name: Po-Yen Chen
	- student_id: b09902061
	- github: [cpy0126](https://github.com/cpy0126)
- member:
	- name: Tien-Sheng Cheng
	- student_id: b09902105
	- github: [chengtiensheng](https://github.com/chengtiensheng)

### Repo
------

- ComputerAgent_<code>$steps</code> ( Just for testing our agent's performance )

  This is a agent copy from a GitHub [othello project](https://github.com/CaseyAlvarado/Zen-Master-Go/blob/a5962f40441ff0b474bb4d16ed505363287c0440/Othello/Othello.py) which using alpha-beta purning and searching the board depending on the $steps we input.

- MyAgentR

  One of our agent. The 'R' means it use a <code>random.randint()</code> function to alternate the result of every game. In this agent, two scored methods are used. First, <code>get_score()</code> function give every position on the board a weight which depends on it's impotance and sum where is occupy by out agent's pieces. For the other method, we try to minimize the legal moves our opponent has after our act. Since these two way all have  a win rate about 80% when playing with RandomAgent, we decide to use the <code>random.randint()</code> function to choose which method will be used in each step. However, we found that this make our win rate descend to about 50%. So we start to develope another way to choose which method will be used in each step.

- MyAgentS

  This agent use DFS(depth first search) algorithm to find out the best move in the next 2~3 moves.During the game,the agent use three different ways to calculate the "score" of different states:
  
  1. weighted-score:In case of some positions are better in our winning strategy,we designed a weighted-board,each position has it's own weight.The function returns the sum of all position's weight our agent is taking now. 


  2. flexibility:One of the winning strategy of reversi is to restrict other's move,so we designed a function <code> Legal_Move</code> ,which can check over the board and finds out all the position we can move.The flexibility funcion is defined by the size of this array.
  

  3. unweighted-score:At the end of game,the score is calculated by counting the number of positions our agent is taking,so this agent is used when the game is nearly over.
  
  We randomly choose from algorithm 1. and 2. in the first 25 steps(with about 90% of possibility to choose 1. 10% of possibility to choose 2. In the last 5 steps, we choose the third algorithm.
 
  Besides all the algorithms above,we noticed that the "corner" of the board ((0,0),(0,7),(7,0),(7,7)) are the most important positions on the board ,so if we can place a piece on these position, we'll do that immediately.

### Prerequsite
```
$ pip install pygame
$ pip install tqdm
$ pip install numpy
```
### Repo structure
```
.
├── README.md
├── agent
│   └── base_agent.py
├── arena.py
├── board.py
├── env.py
├── font
│   ├── LICENSE.txt
│   └── OpenSans-Regular.ttf
├── pygamewrapper.py
├── reversi.py
├── reversi_board.py
└── utils.py
```

### Usage
```
$ git clone https://github.com/cwlin1998/reversi-pygame.git
$ cd reversi-pygame
$ python3 arena.py --time_limit=600000
```

Now you can play with an AI
### Github tutorial 
[Our slide](https://docs.google.com/presentation/d/1X0YmTyj4BNnG7E8saxtG-jH9XLWm8OiFG3L21HhgRwc/edit#slide=id.gacd295469b_2_15)

### Python tutorial

[Our slide](https://docs.google.com/presentation/d/1pyyqS0QBvdS6jl4sLFFINce6fYdUXPpX9f47-3n6AME/edit?usp=sharing)

### Markdown tutorial

[Our slide](https://docs.google.com/presentation/d/1BrGTMmXFdGQpRkhMQs3FPhjOsyPv-EwPOy3bguRlIbI/edit?usp=sharing)



###  Preparation for Team Project
1. [Duplicate this repo](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) and make it private.
> Thanks to [GWFrank](https://github.com/GWFrank) providing the solution.
2. Add your teamates and TA to your repo.
3. Write your member name in your README.
For example:
    ### Team members
    - Team leader:
        - name: Cheng-Wei Lin
        - student_id: r09922078
        - github: [cwlin1998](https://github.com/cwlin1998)
    - member:
        - name: Chi-Ming Chung
        - student_id: r09944021
        - github: [MarvinChung](https://github.com/MarvinChung)

## Todo
- Write an agent for your game:
    - You need to inherit BaseAgent and write your own agent
    ```
    class MyAgent(BaseAgent):
        def step(self, obs, reward):
            // override this function
    ```
    - Put your agent in agent_folder and name it using your team leader's github id with a suffix.
    For example:
    ```
    ├── agent
    │   ├── cwlin1998.py
    │   ├── cwlin1998_func/    # put your other files under this folder
    │   └── base_agent.py 
    ```
    
    - **Your agent should not exceed the time limit (30s) per game, otherwise you lose the game.**
- Test your agent
    ```
    $ python3 arena.py --agent1 cwlin1998.MyAgent --agent2 base_agent.RandomAgent
    ```
- Write your report
  
    - Put your report in README.md. Learn how to write markdown
    
- Work as a team and learn how to use github and read code :100: 

## Grading policy
### Learn Github (60%)
- (**10 %**) Duplicate our repo
    - When your duplicate this repo and add TAs into your repo you get 8 points.
    - You get 2 points when you add your teammates and show their name in README.md.
- (**10 %**) Create your own branch and clean our branches
    - Delete all of our branches except main.
    - Create your own branches.
- (**10 %**) Protect main branch 
    - Merge only when all teammember(not including TAs) approves.
    - Main branch should be clean. No redundacy code and bug.
    - You will need to use git branch and learn how to use git rebase.
- (**10 %**) All members should collaborate together and use pull request.
  
    - Disccus to each other.
- (**10 %**) Use git tag to do version control
    - For example: 
        - tag name: v1.0, v1.1 ....
    - TA will grade your code using the latest tag
- (**10 %**) Write the report in your README.md
    - Describe how you made your agent. Example: What algorithm you use?
    - You can write your report on top of this README.md after forking
        - For example:
            # Reversi Game Project
            ### Team members
            - Team leader:
                - name: Cheng-Wei Lin
                - student_id: r09922078
                - github: [cwlin1998](https://github.com/cwlin1998)
            - member:
                - name: Chi-Ming Chung
                - student_id: r09944021
                - github: [MarvinChung](https://github.com/MarvinChung)
            ### Report
            I don't have time therefore I submit random agent.

### Python coding (40 %) 
- (**10 %**) Your agent can be run
    - You can even copy paste our RandomAgent and change the name to get 10 points. 
- (**10 %**) Pass the baseline
    - We will test your agent agaist RandomAgent. You need to have an at least 80% win rate to get 10 points.
    - **Caution: Please do not exceed time limit(30s per game)**
- (**20 %**) Leaderboard
    - We will test all your agents and you will fight with each others.
    - Your team will get 1 point if you beat another team. (You can get 20 points at most.) Try to beat  your classmates! :punch:
    - Don't give others your code! :no_good:
    - **The leaderboard will be announced.** 
    You have one month for this HW. Good luck!

## QA

1. Put your questions in issues inside this repo.
2. **Bonus:**
    If you find bugs :beetle: in TAs' repo. you can report it with issues and fix it with pull request then you may get bonus points. :thumbsup:
>>>>>>> feature/agent

### Usage
```
$ git clone https://github.com/cwlin1998/reversi-pygame.git
$ cd reversi-pygame
$ python3 arena.py --time_limit=600000
```

Now you can play with an AI
### Github tutorial 
[Our slide](https://docs.google.com/presentation/d/1X0YmTyj4BNnG7E8saxtG-jH9XLWm8OiFG3L21HhgRwc/edit#slide=id.gacd295469b_2_15)

### Python tutorial

[Our slide](https://docs.google.com/presentation/d/1pyyqS0QBvdS6jl4sLFFINce6fYdUXPpX9f47-3n6AME/edit?usp=sharing)

### Markdown tutorial

[Our slide](https://docs.google.com/presentation/d/1BrGTMmXFdGQpRkhMQs3FPhjOsyPv-EwPOy3bguRlIbI/edit?usp=sharing)



###  Preparation for Team Project
1. [Duplicate this repo](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) and make it private.
> Thanks to [GWFrank](https://github.com/GWFrank) providing the solution.
2. Add your teamates and TA to your repo.
3. Write your member name in your README.
For example:
    ### Team members
    - Team leader:
        - name: Cheng-Wei Lin
        - student_id: r09922078
        - github: [cwlin1998](https://github.com/cwlin1998)
    - member:
        - name: Chi-Ming Chung
        - student_id: r09944021
        - github: [MarvinChung](https://github.com/MarvinChung)

## Todo
- Write an agent for your game:
    - You need to inherit BaseAgent and write your own agent
    ```
    class MyAgent(BaseAgent):
        def step(self, obs, reward):
            // override this function
    ```
    - Put your agent in agent_folder and name it using your team leader's github id with a suffix.
    For example:
    ```
    ├── agent
    │   ├── cwlin1998.py
    │   ├── cwlin1998_func/    # put your other files under this folder
    │   └── base_agent.py 
    ```
    
    - **Your agent should not exceed the time limit (30s) per game, otherwise you lose the game.**
- Test your agent
    ```
    $ python3 arena.py --agent1 cwlin1998.MyAgent --agent2 base_agent.RandomAgent
    ```
- Write your report
  
    - Put your report in README.md. Learn how to write markdown
    
- Work as a team and learn how to use github and read code :100: 

## Grading policy
### Learn Github (60%)
- (**10 %**) Duplicate our repo
    - When your duplicate this repo and add TAs into your repo you get 8 points.
    - You get 2 points when you add your teammates and show their name in README.md.
- (**10 %**) Create your own branch and clean our branches
    - Delete all of our branches except main.
    - Create your own branches.
- (**10 %**) Protect main branch 
    - Merge only when all teammember(not including TAs) approves.
    - Main branch should be clean. No redundacy code and bug.
    - You will need to use git branch and learn how to use git rebase.
- (**10 %**) All members should collaborate together and use pull request.
  
    - Disccus to each other.
- (**10 %**) Use git tag to do version control
    - For example: 
        - tag name: v1.0, v1.1 ....
    - TA will grade your code using the latest tag
- (**10 %**) Write the report in your README.md
    - Describe how you made your agent. Example: What algorithm you use?
    - You can write your report on top of this README.md after forking
        - For example:
            # Reversi Game Project
            ### Team members
            - Team leader:
                - name: Cheng-Wei Lin
                - student_id: r09922078
                - github: [cwlin1998](https://github.com/cwlin1998)
            - member:
                - name: Chi-Ming Chung
                - student_id: r09944021
                - github: [MarvinChung](https://github.com/MarvinChung)
            ### Report
            I don't have time therefore I submit random agent.

### Python coding (40 %) 
- (**10 %**) Your agent can be run
    - You can even copy paste our RandomAgent and change the name to get 10 points. 
- (**10 %**) Pass the baseline
    - We will test your agent agaist RandomAgent. You need to have an at least 80% win rate to get 10 points.
    - **Caution: Please do not exceed time limit(30s per game)**
- (**20 %**) Leaderboard
    - We will test all your agents and you will fight with each others.
    - Your team will get 1 point if you beat another team. (You can get 20 points at most.) Try to beat  your classmates! :punch:
    - Don't give others your code! :no_good:
    - **The leaderboard will be announced.** 
    You have one month for this HW. Good luck!

## QA

1. Put your questions in issues inside this repo.
2. **Bonus:**
    If you find bugs :beetle: in TAs' repo. you can report it with issues and fix it with pull request then you may get bonus points. :thumbsup:

