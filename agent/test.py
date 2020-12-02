import random
import pygame
import sys
import copy
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION

class BaseAgent():
    def __init__(self, color = 'black', rows_n = 8, cols_n = 8, width = 600, height = 600):
        self.color = -1 if color=='black' else 1
        self.rows_n = rows_n
        self.cols_n = cols_n
        self.block_len = 0.8 * min(height, width)/cols_n
        self.col_offset = (width - height)/2 + 0.1 * min(height, width) + 0.5 * self.block_len
        self.row_offset = 0.1 * min(height, width) + 0.5 * self.block_len
        

    def step(self, reward, obs):
        """
        Parameters
        ----------
        reward : dict
            current_score - previous_score
            
            key: -1(black), 1(white)
            value: numbers
            
        obs    :  dict 
            board status
            key: int 0 ~ 63
            value: [-1, 0 ,1]
                    -1 : black
                     0 : empty
                     1 : white
        Returns
        -------
        tuple:
            (x, y) represents position, where (0, 0) mean top left. 
                x: go right
                y: go down
        event_type:
            non human agent uses pygame.USEREVENT
        """

        raise NotImplementError("You didn't finish your step function. Please override step function of BaseAgent!")
class MyAgent1(BaseAgent):

    def get_score(self,obs):
        weight = [[90,-60,10,10,10,10,-60,90]
                 ,[-60,-80,5,5,5,5,-80,-60]
                 ,[10,5,1,1,1,1,5,10]
                 ,[10,5,1,1,1,1,5,10]
                 ,[10,5,1,1,1,1,5,10]
                 ,[10,5,1,1,1,1,5,10]
                 ,[-60,-80,5,5,5,5,-80,-60]
                 ,[90,-60,10,10,10,10,-60,90]]
        score = [0,0]
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == self.color:
                    score[0] += weight[i][j]
                if obs[i][j] != self.color and obs[i][j] != 0:
                    score[1] += weight[i][j]
        return score[0]-score[1]
        
    def trans(self,array):
        count = 0
        transarray=[]
        for i in range(8):
            transarray.append([])
            for j in range(8):
                transarray[i].append(array[count])
                count+=1
        return transarray

    def legalMove(self,color,obs):#有bug
        LegalMove=[]
        #print(obs)
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                cobs= self.act(i,j,color,copy.deepcopy(obs))
                #print(i,j,cobs)
                if cobs!=None:
                    LegalMove.append((i,j))
        return LegalMove

    def act(self,x,y,color,obs):
        if obs[x][y]!=0:
            return None
        cobs=copy.deepcopy(obs)
        cobs[x][y]=color

        flipped = False
        row = x
        col = y
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j==0: continue
                row=x
                col=y
                ready_flip = []
                while 0<=col+j<self.cols_n and 0<=row+i<self.rows_n:
                    row+=i
                    col+=j
                    if obs[row][col]==color:
                        while ready_flip:
                            cobs[ready_flip[0][0]][ready_flip[0][1]]=color
                            ready_flip.pop(0)
                            flipped=True
                        break
                    elif obs[row][col]==0: break
                    else:
                        ready_flip.append((row,col))
        if flipped:
            return cobs
        else:
            return None

    def step(self,reward, obs):
        bestMove = self.dfs(self.trans(obs),self.color,3)[0]
        print(bestMove)
        return (self.col_offset + (bestMove[1]) * self.block_len, self.row_offset + (bestMove[0]) * self.block_len), pygame.USEREVENT

    def dfs(self,obs,cur_color,steps):
        if steps == 0 :
            return None,self.get_score(copy.deepcopy(obs))
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        #print('dfs',steps,legal_move)
        if not legal_move:
            return [None,self.get_score(copy.deepcopy(obs))]
        bestmove=[(-1,-1),0]
        my_choose = -10000000
        opponent_choose = 10000000
        print('dfs',steps,'start----')
        print(legal_move)
        moveandscore = []
        for i in range(len(legal_move)):
            print('go dfs',legal_move[i])
            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
            #print(branch)
            temp = self.dfs(branch,-1*cur_color,steps-1)
            print(legal_move[i],'score = ',temp[1])
            moveandscore.append([legal_move[i],temp[1]])
            score =temp[1]
            if cur_color == self.color:
                if my_choose < score:
                    my_choose = score
                    bestmove[0] = legal_move[i]
                    bestmove[1] = score
            else:
                if opponent_choose > score:
                    opponent_choose = score
                    bestmove[0] = legal_move[i]
                    bestmove[1] = score
        print(cur_color,moveandscore)
        print('------end dfs',steps,'bestmove = ',bestmove)
        if bestmove[0]==(-1,-1):
            return [None,self.get_score(copy.deepcopy(obs))]
        return bestmove

if __name__ == "__main__":
    obs={}
    for i in range(64):
        obs[i]=int(input())
    agent1 = MyAgent1()
    agent1.step(0,obs)