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

class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''
    def __init__(self,array):
        '''If the parameter 'board' is left out, then the game board
        is initialized to its typical starting postion. Alternatively,
        a two-dimensional list with a pre-existing starting position
        can be supplied as well. Note that the size of the board is
        10x10, instead of 8x8; this is because leaving a blank ring
        around the edge of the board makes the rest of the code much
        simpler.'''
        self.array = array

    def makeMove(self,row,col,piece):
        ''' Returns None if move is not legal. Otherwise returns an
        updated OthelloBoard, which is a copy of the original.'''

        # A move cannot be made if a piece is already there.
        if self.array[row][col] != empty:
             return None

        # A move cannot be made if the piece "value" is not black or white.
        if piece != black and piece != white:
            return None

        # Make a copy of the board (not just the pointer!)
        bcopy = copy.deepcopy(self.array)
        bcopy[row][col] = piece

        # Ranges for use below
        rowup = range(row+1,size)
        rowdown = range(row-1,-1,-1)
        rowfixed = [row for i in range(size)]
        colup = range(col+1,size)
        coldown = range(col-1,-1,-1)
        colfixed = [col for i in range(size)]

        # Set up ranges of tuples representing all eight directions.
        vectors = [zip(rowup,coldown),zip(rowup,colfixed), \
                zip(rowup,colup), zip(rowdown,coldown), \
                zip(rowdown, colfixed), zip(rowdown,colup), \
                zip(rowfixed,coldown), zip(rowfixed,colup)]

        # Try to make a move in each direction. Record if at least one
        # of them succeeds.
        flipped = False
        for vector in vectors:

            # Determine how far you can go in this direction. If you
            # see the opponent's piece, that's a candidate for
            # flipping: count and keep moving. If you see your own
            # piece, that's the end of the range and you're done. If
            # you see a blank space, you must not have had one of your
            # own pieces on the other end of the range.
            count = 0
            list_vector = list(vector)
            for (r,c) in list_vector:
                if bcopy[r][c] == -1*piece:
                    count += 1
                elif bcopy[r][c] == piece:
                    break
                else:
                    count = 0
                    break

            # If range is nontrivial, then it's a successful move.
            if count > 0:
                flipped = True

            # Actually record the flips.
            for i in range(count):
                r,c = list_vector[i]
                bcopy[r][c] = piece

        if flipped:
            return OthelloBoard(bcopy)
        else:
            return None
    
                         
    def _legalMoves(self,color):
        '''To be a legal move, the space must be blank, and you must take at
        least one piece. Note that this method works by attempting to
        move at each possible square, and recording which moves
        succeed. Therefore, using this method in order to try to limit
        which spaces you actually use in makeMoves is futile.'''
        moves = []
        for i in range(1,size-1):
            for j in range(1,size-1):
                bcopy = self.makeMove(i,j,color)
                if bcopy != None:
                    moves.append((i,j))
        return moves

    def scores(self):
        '''Returns a list of black and white scores for the current board.'''
        score = [0,0]
        for i in range(1,size-1):
            for j in range(1,size-1):
                if self.array[i][j] == black:
                    score[0] += 1
                elif self.array[i][j] == white:
                    score[1] += 1
        return score

    def heuristic(self):
        '''This function just takes the piece value (either 1 or -1) and multiplies it by a weight given
        by the board position.'''
        scoreSum = 0
        for i in range(1,size-1): #rows 
            for j in range(1,size-1):#columns 
                if (((i==1) or (i ==size-1)) and ((j==1) or (j==size-1))):  #all corners are worth 5 times the points 
                    scoreSum += 5*(self.array[i][j])
                elif (((i >=3) and (i<=6)) and ((j==3) or (j==6))) or (((i==4) or (i==5)) and ((j==4) or (j==5))):
                    scoreSum+= 4*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==1) or (j==size-1))) or (((i==1) or (i==size-1)) and ((j>=3) and (j<=6))): 
                    scoreSum += 3*(self.array[i][j])
                elif (((i>=3) and (i<=6)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j>=3) and (j<=6))): 
                    scoreSum += 2*(self.array[i][j])
                elif (((i==1) or (i==size-1)) and ((j==2) or (j==size-2))) or (((i==2) or (i==size-2)) and ((j<=2) or (j>=size-2))):
                    scoreSum += self.array[i][j]
        return scoreSum
            

def trans(array):
    count = 0
    transarray = [[0,0,0,0,0,0,0,0,0,0]]
    for i in range(1,9):
        transarray.append([])
        transarray[i].append(0)
        for j in range(1,9):
            transarray[i].append(array[count])
            count+=1
        transarray[i].append(0)
    transarray.append([0,0,0,0,0,0,0,0,0,0])
    return transarray

class ComputerAgent_3(BaseAgent):
    def step(self,reward,obs):
        transobs = trans(obs)
        bestMove = self.minimax(OthelloBoard(transobs),3,True,1000,1000)[0]
        return (self.col_offset + (bestMove[1]-1) * self.block_len, self.row_offset + (bestMove[0]-1) * self.block_len), pygame.USEREVENT

    def minimax(self, node, depth, maximizing, alpha, beta):
        '''Recursively looks a certain number of plies ahead to determine the best move'''
        if depth == 0 or not node._legalMoves(self.color): # Base case - returns Roxanne heuristic of the board
            return None, self.color * node.heuristic()
        else:
            bestMove = None
            
            if maximizing: # Is it the computer's turn?
                node_legalMoves = node._legalMoves(self.color)
            else:          # Or the opponent's turn?
                node_legalMoves = node._legalMoves(-1*self.color)
                
            for i in node_legalMoves:
                if maximizing:
                    branch = node.makeMove(i[0], i[1], self.color)
                else:
                    branch = node.makeMove(i[0], i[1], -1*self.color)
                    
                nextMove, val = self.minimax(branch, depth-1, not maximizing, alpha, beta)
                val = -val # <---------------------- The tree will look like this:
                                                    #              3
                if val < alpha and maximizing:      #             / \
                    alpha = val                     #           -3  -1 <---- Picks the largest branch
                    bestMove = i                    #           /\  /\       and negates it
                if val < beta and not maximizing:   #          3 1 1 -2
                    beta = val
                    bestMove = i
                if alpha != 1000 and beta != -1000 and alpha <= -beta: # Ignores branches that don't need to be checked
                    break                                              # Sometimes, it's mathematically impossible for certain branches
            if maximizing:                                             #      to be better than other branches, so they become pruned
                return bestMove, alpha
            return bestMove, beta

class ComputerAgent_1(BaseAgent):
    def step(self,reward,obs):
        transobs = trans(obs)
        bestMove = self.minimax(OthelloBoard(transobs),1,True,1000,1000)[0]
        return (self.col_offset + (bestMove[1]-1) * self.block_len, self.row_offset + (bestMove[0]-1) * self.block_len), pygame.USEREVENT

    def minimax(self, node, depth, maximizing, alpha, beta):
        '''Recursively looks a certain number of plies ahead to determine the best move'''
        if depth == 0 or not node._legalMoves(self.color): # Base case - returns Roxanne heuristic of the board
            return None, self.color * node.heuristic()
        else:
            bestMove = None
            
            if maximizing: # Is it the computer's turn?
                node_legalMoves = node._legalMoves(self.color)
            else:          # Or the opponent's turn?
                node_legalMoves = node._legalMoves(-1*self.color)
                
            for i in node_legalMoves:
                if maximizing:
                    branch = node.makeMove(i[0], i[1], self.color)
                else:
                    branch = node.makeMove(i[0], i[1], -1*self.color)
                    
                nextMove, val = self.minimax(branch, depth-1, not maximizing, alpha, beta)
                val = -val # <---------------------- The tree will look like this:
                                                    #              3
                if val < alpha and maximizing:      #             / \
                    alpha = val                     #           -3  -1 <---- Picks the largest branch
                    bestMove = i                    #           /\  /\       and negates it
                if val < beta and not maximizing:   #          3 1 1 -2
                    beta = val
                    bestMove = i
                if alpha != 1000 and beta != -1000 and alpha <= -beta: # Ignores branches that don't need to be checked
                    break                                              # Sometimes, it's mathematically impossible for certain branches
            if maximizing:                                             #      to be better than other branches, so they become pruned
                return bestMove, alpha
            return bestMove, beta

def get_score(obs,color):
    weight = [90,-60,10,10,10,10,-60,90
             ,-60,-80,5,5,5,5,-80,-60
             ,10,5,1,1,1,1,5,10
             ,10,5,1,1,1,1,5,10
             ,10,5,1,1,1,1,5,10
             ,10,5,1,1,1,1,5,10
             ,-60,-80,5,5,5,5,-80,-60
             ,90,-60,10,10,10,10,-60,90]
    score = [0,0]
    for i in obs:
        if obs[i] == -1:
            score[0] += weight[i]
        if obs[i] == 1:
            score[1] += weight[i]
    return score[0] if color ==-1 else score[1]


class MyAgent(BaseAgent):
    
    def legalMove():
        

    def act():
        


    def step():
        

    def empty():
        

    def dfs():
        

if __name__ == "__main__":
    agent = ComputerAgent()
    print(agent.step(None, None))
