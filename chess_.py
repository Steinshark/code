import chess
import random
import sys
import string
class Chess_Game:
    def __init__(self):
        try:
            self.games = sys.argv[1]
            self.fname = sys.argv[2]
            self.file = open(sys.argv[2],'a')
        except IndexError:
            pass
    def random_move(self,board):
        sample_size = board.legal_moves.count()
        move = ''
        our_num = random.randint(0,sample_size-1)
        for n in range(0,our_num-1):
            move = next(iter(board.legal_moves))
        return str(move)

    def best_move(self):
        pass

    def build_data_file(self):
        for i in range(0,int(self.games)):
            self.write_game()
            if i % 100 == 0:
                print("games written : " + str(i))

    def write_game(self):
        game = '{'
        board = chess.Board(chess.STARTING_FEN)
        while board.outcome() is None:
            move = self.random_move(board)
            game+=str(move)+ ','
            board.push_san(move)
        self.file.write(str(game)+str(board.outcome())+'}\n')

    def interpret_game(self,raw_game):
        move_seq = raw_game[1:raw_game.index('O')]
        moves = []
        n = 0
        while n < len(move_seq)-4:
            move = str(move_seq[n])+str(move_seq[n+1])+str(move_seq[n+2])+str(move_seq[n+3])
            if (not (n+4 == len(move_seq)-1)) and str(move_seq[n+4]) in string.ascii_lowercase+string.ascii_uppercase:
                move += str(move_seq[n+4])
                print(move)
                n += 5
            n += 4
            moves.append(move)
        print(move_seq[-4:])
        print(moves[-1])

    def read_games(self,fname):
        file = open(fname,'r')

        for line in file.readlines():
            print(line)
            self.interpret_game(line)
            input()
instance = Chess_Game()
instance.build_data_file()
