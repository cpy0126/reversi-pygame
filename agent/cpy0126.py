import random
import pygame
import sys
import copy
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
black=-1
white=1
empty=0
size = 10
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
    
class HumanAgent(BaseAgent):
    def step(self, reward, obs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                return event.pos, event.type
            if event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos, pygame.USEREVENT

        return (-1, -1), None

class RandomAgent(BaseAgent):
    def legalMove(self,color,obs):
        LegalMove=[]
        for i in range(self.rows_n*self.cols_n):
            branch,p = self.act(i,color,obs)
            if branch and p:
                LegalMove.append(i)
        return LegalMove

    def act(self,action,color,obs):
        if obs[action]!=0:
            return None,False
        cobs=obs.copy()
        cobs[action]=color
        flipped = False
        row = action//self.rows_n
        col = action%self.rows_n
        for i in range(-1,2):
            for j in range(-1,2):
                if i==0 and j==0: continue
                x=row
                y=col
                ready_flip = []
                while 0<=y+j<self.cols_n and 0<=x+i<self.rows_n:
                    x+=i
                    y+=j
                    if obs[x*8+y]==color:
                        while ready_flip:
                            cobs[ready_flip[0]]=color
                            ready_flip.pop(0)
                            flipped=True
                        break        
                    elif cobs[x*8+y]==0: break
                    else:
                        ready_flip.append(x*8+y)
        return cobs,flipped
    def step(self, reward, obs):
        legal = self.legalMove(self.color,obs)
        index = random.randint(0,len(legal)-1)
        return (self.col_offset + legal[index]%self.cols_n * self.block_len, self.row_offset + legal[index]//self.rows_n * self.block_len), pygame.USEREVENT

class MyAgentR(BaseAgent):

    def get_score(self,obs):
        weight =[[500,-25,10,5,5,10,-25,500],
                [-25,-45,1,1,1,1,-45,-25],
                [10,1,3,2,2,3,1,10],
                [5,1,2,1,1,2,1,5],
                [5,1,2,1,1,2,1,5],
                [10,1,3,2,2,3,1,10],
                [-25,-45,1,1,1,1,-45,-25],
                [500,-25,10,5,5,10,-25,500]]
        score = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == self.color:
                    score += weight[i][j]
        return score
        
    def trans(self,array):
        count = 0
        transarray=[]
        for i in range(8):
            transarray.append([])
            for j in range(8):
                transarray[i].append(array[count])
                count+=1
        return transarray

    def legalMove(self,color,obs):
        LegalMove=[]
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                cobs= self.act(i,j,color,copy.deepcopy(obs))
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

    def empty(self,obs):
        count = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == 0:
                    count+=1
        return count
    def step(self,reward, obs,control=10):
        rand = random.randint(0,control)
        if rand:#empty>=40
            bestMove = self.weight(self.trans(obs),self.color)
        else:
            bestMove = self.moveplace(self.trans(obs),self.color)
        return (self.col_offset + (bestMove[1]) * self.block_len, self.row_offset + (bestMove[0]) * self.block_len), pygame.USEREVENT

    def weight(self,obs,cur_color):
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        max_score = -1000
        if not legal_move :
            return None
        bestmove = None
        corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in range(len(legal_move)):
            for j in range(4): #check corners
                if legal_move[i]==corner[j]:
                    branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
                    return legal_move[i]

            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
            score = self.get_score(branch)
            if score >= max_score:
                max_score = score
                bestmove = legal_move[i]

        return bestmove

    def moveplace(self,obs,cur_color):
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        min_score = 1000
        if not legal_move :
            return None
        bestmove = None
        corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in range(len(legal_move)):
            for j in range(4): #check corners
                if legal_move[i]==corner[j]:
                    branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
                    return legal_move[i]

            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
            score = len(self.legalMove(cur_color,branch))
            if score <= min_score:
                min_score = score
                bestmove = legal_move[i]

        return bestmove

class MyAgentS(BaseAgent):

    def get_score(self,obs):
        weight = [[500,-25,10,5,5,10,-25,500],
                    [-25,-45,1,1,1,1,-45,-25],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-25,-45,1,1,1,1,-45,-25],
                    [500,-25,10,5,5,10,-25,500]]
        score = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == self.color:
                    score += weight[i][j]
        return score
        
    def trans(self,array):
        count = 0
        transarray=[]
        for i in range(8):
            transarray.append([])
            for j in range(8):
                transarray[i].append(array[count])
                count+=1
        return transarray

    def legalMove(self,color,obs):
        LegalMove=[]
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                cobs= self.act(i,j,color,copy.deepcopy(obs))
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

    def empty(self,obs):
        count = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == 0:
                    count+=1
        return count

    def step(self,reward, obs, control=20):
        empty = self.empty(self.trans(obs))
        if empty>=control:
            bestMove = self.weight(self.trans(obs),self.color)
        else:
            bestMove = self.moveplace(self.trans(obs),self.color)
        return (self.col_offset + (bestMove[1]) * self.block_len, self.row_offset + (bestMove[0]) * self.block_len), pygame.USEREVENT

    def weight(self,obs,cur_color):
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        max_score = -1000
        if not legal_move :
            return None
        bestmove = None
        corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in range(len(legal_move)):

            for j in range(4): #check corners
                if legal_move[i]==corner[j]:
                    branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
                    return legal_move[i]

            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
            score = self.get_score(branch)
            if score >= max_score:
                max_score = score
                bestmove = legal_move[i]

        return bestmove

    def moveplace(self,obs,cur_color):
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        min_score = 1000
        if not legal_move :
            return None
        bestmove = None
        corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in range(len(legal_move)):

            for j in range(4): #check corners
                if legal_move[i]==corner[j]:
                    branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
                    return legal_move[i]

            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
            score = len(self.legalMove(cur_color,branch))
            if score <= min_score:
                min_score = score
                bestmove = legal_move[i]

        return bestmove

class MyAgent(BaseAgent):

    def get_score1(self,obs):
        weight =[[500,-25,10,5,5,10,-25,500],
                [-25,-45,1,1,1,1,-45,-25],
                [10,1,3,2,2,3,1,10],
                [5,1,2,1,1,2,1,5],
                [5,1,2,1,1,2,1,5],
                [10,1,3,2,2,3,1,10],
                [-25,-45,1,1,1,1,-45,-25],
                [500,-25,10,5,5,10,-25,500]]
        score = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == self.color:
                    score += weight[i][j]
        return score

    def get_score2(self,obs):
        num=0
        for i in range(self.rows_n):
                for j in range(self.cols_n):
                    if obs[i][j] == self.color:
                        num+=1

        return num
    
    def trans(self,array):
        count = 0
        transarray=[]
        for i in range(8):
            transarray.append([])
            for j in range(8):
                transarray[i].append(array[count])
                count+=1
        return transarray

    def legalMove(self,color,obs):
        LegalMove=[]
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                cobs= self.act(i,j,color,copy.deepcopy(obs))
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

    def empty(self,obs):
        count = 0
        for i in range(self.rows_n):
            for j in range(self.cols_n):
                if obs[i][j] == 0:
                    count+=1
        return count

    def step(self,reward, obs, control=10):
        empty=self.empty(self.trans(obs))
        rand = random.randint(0,control)
        if empty<10:
            bestMove = self.dfsW2(self.trans(obs),self.color,2,2)
        else:
            if rand:
                bestMove = self.dfsW1(self.trans(obs),self.color,2,2)
            else:
                bestMove = self.dfsS(self.trans(obs),self.color)
        return (self.col_offset + (bestMove[1]) * self.block_len, self.row_offset + (bestMove[0]) * self.block_len), pygame.USEREVENT

    def dfsW2(self,obs,cur_color,num,cur_num):
        legal_move= self.legalMove(cur_color,copy.deepcopy(obs))
        max_score = -1000000 *cur_color*self.color
        bestmove = (0,0)
        score=0
        if not legal_move :
            return max_score
        for i in range(len(legal_move)):
            if (cur_num==num) and ((legal_move[i][0]==0) or (legal_move[i][0]==7) ) and ((legal_move[i][1]==0) or (legal_move[i][1]==7)):
                return legal_move[i]
            if cur_num > 0 :
                branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
                score=self.dfsW2(branch,-cur_color,num,cur_num-1)
            if cur_num == 0 :
                branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
                score=self.get_score2(branch)
            #if cur_num == num :
                #print(i,score,max_score)
            if cur_color==self.color and score >= max_score:
                max_score = score
                bestmove = legal_move[i]
                #print(max_score)
            if cur_color==-self.color and score <= max_score:
                max_score = score
                bestmove = legal_move[i]
                #print(max_score)
        if cur_num==num :
            return bestmove
        return score

    def dfsW1(self,obs,cur_color,num,cur_num):
        legal_move= self.legalMove(cur_color,copy.deepcopy(obs))
        max_score = -1000000 *cur_color*self.color
        bestmove = (0,0)
        score=0
        if not legal_move :
            return max_score
        for i in range(len(legal_move)):
            if (cur_num==num) and ((legal_move[i][0]==0) or (legal_move[i][0]==7) )and ((legal_move[i][1]==0) or (legal_move[i][1]==7)):
                return legal_move[i]
            if cur_num > 0 :
                branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
                score=self.dfsW1(branch,-cur_color,num,cur_num-1)
            if cur_num == 0 :
                branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
                score=self.get_score1(branch)
            #if cur_num == num :
                #print(i,score,max_score)
            if cur_color==self.color and score >= max_score:
                max_score = score
                bestmove = legal_move[i]
                #print(max_score)
            if cur_color==-self.color and score <= max_score:
                max_score = score
                bestmove = legal_move[i]
                #print(max_score)
        if cur_num==num :
            return bestmove
        return score
    
    def dfsS(self,obs,cur_color):
        legal_move = self.legalMove(cur_color,copy.deepcopy(obs))
        min_score = 1000
        if not legal_move :
            return None
        bestmove = None
        corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in range(len(legal_move)):

            for j in range(4): #check corners
                if legal_move[i]==corner[j]:
                    branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))
                    return legal_move[i]

            branch = self.act(legal_move[i][0],legal_move[i][1],cur_color,copy.deepcopy(obs))#put the legal move on board
            score = len(self.legalMove(cur_color,branch))
            if score <= min_score:
                min_score = score
                bestmove = legal_move[i]

        return bestmove

        

if __name__ == "__main__":
    agent = ComputerAgent()
    print(agent.step(None, None))
