import time
import Goban
from random import choice
import math
import Model
model = Model.import_model()
def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() peut nous donner un itérateur (quand on
    l'utilise avec pychess).'''
    return choice(list(b.generate_legal_moves()))

def deroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()

# board = Goban.Board()
# deroulementRandom(board)

''' Exemple de déroulement random avec weak_legal_moves()'''

def weakRandomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles mais attention, dans ce cas
    weak_legal_moves() peut renvoyer des coups qui entrainent des super ko. Si on prend un coup au hasard
    il y a donc un risque qu'il ne soit pas légal. Du coup, il faudra surveiller si push() nous renvoie
    bien True et sinon, défaire immédiatement le coup par un pop() et essayer un autre coup.'''
    return choice(b.weak_legal_moves())

def weakDeroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement en utilisant les coups weak_legal_moves().

    Ce petit exemple montre comment utiliser weak_legal_moves() plutot que legal_moves(). Vous y gagnerez en efficacité.'''

    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return

    while True:
        # push peut nous renvoyer faux si le coup demandé n'est pas valide à cause d'un superKo. Dans ce cas il faut
        # faire un pop() avant de retenter un nouveau coup
        valid = b.push(weakRandomMove(b))
        if valid:
            break
        b.pop()
    weakDeroulementRandom(b)
    b.pop()

def Evaluate_board(b):
    if(b.player_name == "black"):

        #return b.compute_score()[0]
        return Model.predection(b._historyMoveNames,model)
    #return b.compute_score()[1]
    return 1 - Model.predection(b._historyMoveNames,model)

def minmax(b,ismin=True,prof=0):
    if b.is_game_over():
        return b.result()[0]
    if prof>0:
        return Evaluate_board(b)

    if ismin:
        best_score = -99999
        choices = list(b.generate_legal_moves())
        for c in choices:
            b.push(c)
            score = int(minmax(b,False,prof+1))
            b.pop()
            best_score = max(best_score,score)

        return best_score
    else:

        best_score = 99999
        choices = list(b.generate_legal_moves())
        for c in choices:
            b.push(c)
            score = int(minmax(b,True,prof+1))
            b.pop()
            best_score = min(best_score,score)

        return best_score

def alpha_beta(b,ismin=True,prof = 0,alpha=-math.inf,beta=math.inf):
    if b.is_game_over():
        return b.result()[0]
    if prof>0:
        return Evaluate_board(b)


    if ismin:
        best_score = - math.inf
        choices = list(b.generate_legal_moves())
        for c in choices:
            b.push(c)
            score = int(alpha_beta(b,False,prof+1,alpha,beta))
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
            score = int(alpha_beta(b,True,prof+1,alpha,beta))
            b.pop()
            best_score = min(best_score,score)
            beta = min(beta,best_score)
            if alpha >= best_score :
                return best_score

        return best_score

def bestMove(b):
    best_score = - math.inf
    deja_vu = set()
    best_move = 0
    while(len(deja_vu)< (len(b.generate_legal_moves()) //2)):
        c = randomMove(b)
        if(c not in deja_vu):
            b.push(c)
            score = int(alpha_beta(b,False,0,-math.inf,math.inf))
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

board = Goban.Board()
# board.push(randomMove(board))
board.pretty_print()
print("score ",board.compute_score())
# print("minmax ",minmax(board,True,0))
# print("possibilities ", list(board.generate_legal_moves()))
bm = bestMove(board)
print("best move ", bm)
board.push(bm)
board.pretty_print()
# deroulementRandom(board)


while(not board.is_game_over()):

    bm = bestMove(board)
    board.push(bm)
    board.pretty_print()
    board.push(randomMove(board))
    board.pretty_print()
    print("best move ", bm)
    print("game is over ? : ",board.is_game_over())

if board.is_game_over():
    print("Resultat : ", board.result())