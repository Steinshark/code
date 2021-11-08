import chess
import random
import time 
import math 
class Chess_Game:
    def __init__(self):
        self.board = chess.Board()
        self.moves = list()
        self.game_over = False
        self.players = ['white','black']
        self.games=[]
    def random_move(self):
        sample_size = self.board.legal_moves.count()
        self.moves = [move for move in iter(self.board.legal_moves)]
        return str(self.moves[random.randint(0,sample_size-1)])

    def best_move(self):
        pass
    def play(self):
        self.board = chess.Board(chess.STARTING_FEN)
        self.game_over = False
        game = '{'
        while not self.game_over:
            move = self.random_move()
            self.board.push_san(move)
            game+=str(move)
            self.check_game()
        res = self.board.outcome()
        game+=','+str(res)+'/n'
        self.games.append(game)        


    def check_game(self):
        if self.board.outcome() is None:
            return
        else:
            self.game_over = True
    
    def write_game(self):
        file = open('games','w')
        for item in self.games:
            file.write(item)
        return

c = Chess_Game()
i = 0
while True:
    c.play()
    print(i:=i+1)
c.write_game()
