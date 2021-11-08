import chess
import random
import copy

class Engine:
    def __init__(self):
        self.board = chess.Board()
        self.current_best_eval = 0
        self.depth = 0

        self.search_space(self.board,3)

    def search_space(self,board,depth):
        for depth in [i for i in range(0,depth)]:
            print(self.mini_max(True,self.board,0,depth,None))



    def mini_max(self,maximizing,board,cur_depth,max_depth,move_passed):
        print('call: ' + str(cur_depth) + " out of: " + str(max_depth))
        print(board)

        if cur_depth == max_depth:
            return self.evaluate(board), move_passed

        evals = {}
        moves = [move for move in iter(board.legal_moves)]

        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.push_san(str(move))
            print(new_board)
            evals[move] = self.mini_max(not maximizing,new_board,cur_depth+1,max_depth,move)
        print(evals)


        if maximizing:
            print(evals)
            input()
            best_move = max(evals,key=evals.get)
            best_eval = evals[best_move][0]
            return  best_eval, best_move
        else:
            print(evals)
            input()
            best_move = min(evals,key=evals.get)
            best_eval = evals[best_move][0]
            return  best_eval, best_move


    def evaluate(self,board):
        return random.randint(-2,2)


engine = Engine()
