# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
import math

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def Evaluate_board(self,b):
        if(self._mycolor == Goban.Board._BLACK):
            return b.compute_score()[0]
        return b.compute_score()[1]
    def randomMove(self,b):
        return choice(list(b.generate_legal_moves()))

    def alpha_beta(self,b,ismin=True,prof = 0,alpha=-math.inf,beta=math.inf):
        if b.is_game_over():
            return b.result()[0]
        if prof>0:
            return self.Evaluate_board(b)

        
        if ismin:
            best_score = - math.inf
            choices = list(b.generate_legal_moves())
            for c in choices:
                b.push(c)
                score = int(self.alpha_beta(b,False,prof+1,alpha,beta))
                b.pop()
                best_score = max(best_score,score)
                alpha = max(alpha,best_score)
                if alpha >= best_score :
                    return best_score
        
            return best_score
        else:
            
            best_score = math.inf
            choices = list(b.generate_legal_moves())
            for c in choices:
                b.push(c)
                score = int(self.alpha_beta(b,True,prof+1,alpha,beta))
                b.pop()
                best_score = min(best_score,score)
                beta = min(beta,best_score)
                if alpha >= best_score :
                    return best_score
        
            return best_score

    def bestMove(self,b): 
        best_score = - math.inf
        deja_vu = set()
        best_move = 0
        while(len(deja_vu)< (len(b.generate_legal_moves()) //2)):
            c = self.randomMove(b)
            if(c not in deja_vu):
                b.push(c)
                score = int(self.alpha_beta(b,False,0,-math.inf,math.inf))
                b.pop()
                deja_vu.add(c)
                if score > best_score:
                    best_score = score
                    best_move = c
        # for c in list(b.generate_legal_moves()):
        #     # print("calculating score")
        #     score = int(minmax(b,False,0))
        #     # print("score is " , score," and best score is ", best_score)
        #     b.pop()
        #     if score > best_score:
        #         best_score = score
        #         best_move = c
        return best_move

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        move = self.bestMove(self._board)
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



