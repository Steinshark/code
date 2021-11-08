import random


class Board:
    def __init__(self):
        self.square = [[None,None,None],[None,None,None],[None,None,None]]
        self.filled = []
        self.game_over = False
        self.next_mov = '1'
        self.on_player = 'x'
        self.winner = None
        self.moves = 0

    def get_mov_input(self):
        mov = input()
        row = ord(mov[0]) - 97
        col = int(mov[1])

        print(row)
        print(col)

        if not self.square[row][col] == None:
            return False
        self.square[row][col] = self.on_player
        if self.on_player == 'x':
            self.on_player = 'o'
        else:
            self.on_player = 'x'

        self.game_over,self.winner = self.check_win()
        return True

    def play_mov(self,mov):
        row = ord(mov[0]) - 97
        col = int(mov[1])
        if not self.square[row][col] == None:
            return False
        self.square[row][col] = self.on_player
        if self.on_player == 'x':
            self.on_player = 'o'
        else:
            self.on_player = 'x'

        self.game_over,self.winner = self.check_win()
        return True

    def check_mov(self,mov):
        row = ord(mov[0]) - 97
        col = int(mov[1])
        if not self.square[row][col] == None:
            return False
        return True

    def check_win(self):
        for row in self.square:
            if not None in row:
                if not 'x' in row:
                    return True,'o'
                elif not 'o' in row:
                    return True, 'x'
        for col in [0,1,2]:
            row = [self.square[0][col], self.square[1][col], self.square[2][col]]
            if not None in row:
                if not 'x' in row:
                    return True,'o'
                elif not 'o' in row:
                    return True, 'x'


        if self.square[0][0] == self.square[1][1] and self.square[1][1] == self.square[2][2] and not None in [self.square[1][1]]:
            return True, self.square[0][0]
        elif self.square[0][2] == self.square[1][1] and self.square [1][1] == self.square[2][0] and not None in [self.square[1][1]]:
            return True, self.square[0][2]
        return False, None

    def translate_to_array(self):
        list = []
        for row in self.square:
            for item in row:
                if item == None:
                    list.append(0)
                elif item == 'x':
                    list.append(1)
                elif item == 'o':
                    list.append(-1)
                else:
                    print("Error building list after finding " + str(item))
                    return -1
        return list
    def __repr__(self):
        master_str = ''
        for row in self.square:
            master_str += "|"
            for item in row:
                try:
                    master_str += item
                except TypeError:
                    master_str += " "
                master_str += "|"
            master_str += "\n"
        return master_str
def play():
    game = Board()
    while not game.game_over:
        while not (res := game.get_mov_input()):
            game.get_mov_input()
        print(game)
    print("GAME OVER")
    print(game.winner)
