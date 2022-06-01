# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

from time import time
import Goban 
from random import choice , shuffle
from playerInterface import *
import math



class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of legalMoves given by legal_legalMoves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''
    
    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.starting= [20,24,40,56,60]
        self.cutoff = False
        self.TIME_LIMIT = 0.5
 

    def alphaBeta(self,board,isMaxi, depth,alpha,beta,startingTime,deadline) :
        
        legalMoves = board.generate_legal_moves()
        result = self.evaluate(board)
        currentTime =time()
        elapsedTime = (currentTime - startingTime)
        shuffle(legalMoves)
        if (elapsedTime >= deadline) :
            self.cutoff = True
            return result
        if (self.cutoff or board.is_game_over() or (depth == 0) or (len(legalMoves) == 0) or (result >= 20000) or (result <= -20000)) :
            return result
        if (isMaxi):
            for m in legalMoves :
                board.push(m)
                alpha = max([alpha, self.alphaBeta(board, depth - 1,False, alpha, beta, startingTime, deadline)])
                board.pop()
                if (beta <= alpha) :
                    break
            return alpha

        else :
            for m in legalMoves :
                board.push(m)
                beta = min([beta, self.alphaBeta(board, depth - 1,True, alpha, beta, startingTime, deadline)])
                board.pop()
                if (beta <= alpha) :
                    break
            return beta
    def IDS(self,board,deadline):
        
        begin = time()
        finishTime = begin + deadline
        depth = 1
        result = 0
        while 1:
            now =time()
            if (now >= finishTime) :
                break
            self.cutoff=False
            resultSh = self.alphaBeta(board, depth,True, float("-inf"),  float("inf"), now, finishTime - now)
            if (resultSh >= 20000) :
                return resultSh
            result = resultSh
            depth+=1  
        return result

    def NextMove(self,board):

        # if len(self.starting)>0:
        #     move = self.starting[0]
        #     self.starting.remove(move)
        #     print("move ... ", move)
        #     return move



        # for i in self.starting:            
        #     self.starting.remove(i)
        #     print("boardiiiiii : ",board[i])
        #     if board[i]:
        #         return i
        myChoiceMove = None
        maximum =float("-inf")
        beginTime = time()
        legalMoves = board.generate_legal_moves()
        #remove PASS
        legalMoves.remove(-1)
        shuffle(legalMoves)
        if (len(legalMoves)<81) :
            black_score, white_score = board.compute_score()
            if (self._mycolor==1) :
                if board._lastPlayerHasPassed and black_score> white_score :
                    return -1
            if (self._mycolor==2) :
                if board._lastPlayerHasPassed and black_score< white_score :
                    return -1
            if len(legalMoves)==0 :
                return -1

        if len(legalMoves)>0 :
            for m in legalMoves :
                board.push(m)
                limitSearchTime =((self.TIME_LIMIT) / len(legalMoves))
                gain = self.IDS(board, limitSearchTime)
                board.pop()

                if (gain >= 20000) :
                    return (m)
                if (gain > maximum) :
                    maximum = gain
                    myChoiceMove = m
          
        else :
            myChoiceMove=-1
        print("tooked time for choosing move :",time()-beginTime, " score=",maximum ," choice " , myChoiceMove)
        return myChoiceMove
    
    @staticmethod
    def neighbor(st) :
        pos = Goban.Board.unflatten(st)
        neighbors = ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1))
        n=[]
        for i in neighbors :
            if (i[0] >= 0 and i[0] < 9) and (i[1] >= 0 and i[1] < 9):
                n.append(Goban.Board.flatten(i))
        return(n)

    @staticmethod
    def getStoneGroup(b,st,color,done,v):
        v.append(st)
        neighbors=myPlayer.neighbor(st)
        neighbors=list(set(neighbors) - set(done))
        for c in neighbors :
            done = list(dict.fromkeys(done))
            if b[c]==color  :
                done.append(c)
                myPlayer.getStoneGroup(b,c,color,done,v)
            else : 
                done.append(c)
        v = list(dict.fromkeys(v))
        return (v)

    @staticmethod
    def getAllGroups(b,my_color,oppo_color):
        my_group=[]
        oppo_group=[]
        for i in range(81) :
            if b[i]==my_color :
                fait=False
                for h in my_group :
                    if i in h :
                        fait=True
                        break
                if fait==False :
                    v=myPlayer.getStoneGroup(b,i,my_color,[i],[])
                    my_group.append(v)
            elif b[i]==oppo_color :
                fait=False
                for h in oppo_group :
                    if i in h :
                        fait=True
                        break
                if fait==False :
                    v=myPlayer.getStoneGroup(b,i,oppo_color,[i],[])
                    oppo_group.append(v)
        return(my_group,oppo_group)

    def getGroupLiberties (b,gr,oppo,i=0) :
        k=[]
        for i in gr :
            v=myPlayer.neighbor(i)
            v=list(set(v) - set(gr))
            k=k+v
        k = list(dict.fromkeys(k))
        liberties_degree=0
        opp_neighbor=0
        for i in k :
            if b[i]==oppo :
                opp_neighbor+=1
            elif b[i]==0 :
                liberties_degree+=1
        return (liberties_degree)

    def getAllGroupsLiberties(b,groups,oppo) :
        v=[]
        for group in groups :
            v.append(myPlayer.getGroupLiberties(b,group,oppo))
        return v


    def evaluate(self,board) :

        b=list(board)
        empty=b.count(0)
        win_score=100-empty

        for i in self.starting:
            if b[i]==self._mycolor :
                self.starting.remove(i)
                return(20000)

        black_score, white_score = self._board.compute_score()
        if (self._mycolor==1):
            my_score, oppo_score = self._board.compute_score()
        else :
            oppo_score,my_score  = self._board.compute_score()
        if ((my_score)>=(oppo_score*2) and oppo_score >4):
            return(20000)
        oppo_color=self._board.flip(self._mycolor)
        my_groups,oppo_groups=myPlayer.getAllGroups(b,self._mycolor,oppo_color)
        my_groups_liberties=myPlayer.getAllGroupsLiberties(b,my_groups,oppo_color)
        oppo_groups_librties=myPlayer.getAllGroupsLiberties(b,oppo_groups,self._mycolor)
        for g in my_groups_liberties :
            if g<=1 : 
                return((win_score-10000) / 2) 
        pt=0
        for g in oppo_groups_librties :
            if g==1 : 
                win_score=win_score +50
            if g==0 :
                pt+=1
                if (pt==2) :
                    return(20000)
                else :
                    win_score+=100
        for me in range(len(my_groups)) :
            if len(my_groups[me])>=2 :
                win_score+=len(my_groups[me])*my_groups_liberties[me]+my_groups_liberties[me]*5+20
        for op in range(len(oppo_groups)) :
            win_score=win_score-len(oppo_groups[op])*oppo_groups_librties[op] 
        # Calculate scores for groups 
        my_groups_2liberties=my_groups_liberties.count(2)
        oppo_groups_2liberties= oppo_groups_librties.count(2)
        groups_score =oppo_groups_2liberties- my_groups_2liberties
        # calcule liberties's score
        liberties_group=sum(my_groups_liberties)-sum(oppo_groups_librties)

        return win_score + groups_score  + liberties_group 
    def getPlayerName(self):
        return "Omar & Sana"
    def getPlayerMove(self):
        self.TIME_LIMIT=0.5
        self.cutoff=False

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        move = self.NextMove(self._board)
        
        self._board.push(move)
        
        # New here: allows to consider internal representations of legalMoves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 
        if(Goban.Board.flatten(move) in self.starting):
            self.starting.remove(Goban.Board.flatten(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


