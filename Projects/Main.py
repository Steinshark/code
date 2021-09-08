import pygame
import time
## TESING STRING ##
class Game:
    def __init__(self):
        self.board = Board()
        pygame.init()
        self.window = pygame.display.set_mode((1900, 1060))
        pygame.display.set_caption("Chess Game!!")

        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill((230, 230, 230))
        self.clock = pygame.time.Clock()
        self.running = True
        self.showing_piece = None

		# THis is all of the games
        self.blits = list()
        self.deletes = list()

    def play(self):
        self.move = "white"
        self.blits.append((self.board.board_image, (100, 200)))

        #   init pieces
        for piece in self.board.pieces:
            self.blits.append(((piece.image), piece.get_loc()))

        while self.running:
            # Make suyre background is black
            self.background.fill((230, 230, 230))
            for item in self.blits:
                img, loc = item
                self.window.blit(img, loc)

            #update all next moves
            for piece in self.board.pieces:
                piece.next_moves()

            for event in pygame.event.get():
                #check if we quit
                if event.type == pygame.QUIT:
                    pygame.quit()

                #check if we clicked a piece
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos

                    # Toggle showing a piece moves
                    for piece in self.board.pieces:
                        if piece.is_in_rect(x, y):
                            # Second click to untoggle piece
                            if self.showing_piece == piece:
                                for next_move in self.deletes:
                                    self.blits.remove(next_move)
                                self.showing_piece = None
                                self.deletes = list()
                            else:
                                self.showing_piece = piece
                                row, col = self.showing_piece.position
                                print(str(row) + " " + str(col))
                                for next_move in self.showing_piece.nextmoves:
                                    print(next_move)
                                    self.blits.append((next_move.img, next_move.get_loc()))
                                    self.deletes.append((next_move.img, next_move.get_loc()))
                    #check for moving piece
                    if not self.showing_piece is None:
                        print(x, y)
                        for move in self.showing_piece.nextmoves:
                            move.x, movey = move.location
                            if move.x == x and move.y == y:
                                print("legal")


            pygame.display.update()
            time.sleep(.01)


class Move:
    def __init__(self, location):
        self.location = location
        self.img = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\dot.png")

    def get_loc(self):
        x, y = self.location
        pos = (int(ord(x) - 65) * Board.scale_x + Board.offset_x, (9 - int(y)) * Board.scale_y + Board.offset_y)
        return pos

class Piece:
    def __init__(self, position, color):
        self.position = position
        self.location = self.get_loc()
        self.color = color
        self.image = None
        self.nextmoves = []
        self.showingmoves = False

    def next_moves(self):
        pass

    def __str__(self):
        return self.position

    def get_loc(self):
        x, y = self.position
        pos = (int(ord(x)-65)*Board.scale_x + Board.offset_x, (9-int(y))*Board.scale_y + Board.offset_y)
        return pos

    def is_in_rect(self, x, y):
        px, py = self.position
        piece_x, piece_y = (int(ord(px)-65)*Board.scale_x + Board.offset_x, (9-int(py))*Board.scale_y + Board.offset_y)
        if (x > piece_x) and (x < (piece_x + Board.scale_x)):
            if (y > piece_y) and (y < (piece_y + Board.scale_y)):
                return True
        return False

    def toggle_showmoves(self):
        if self.showingmoves:
            self.showingmoves = False
        else:
            self.showingmoves = True


class King(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\King_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\King_b.png")

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        for row_n in range(-1, 2):
            for col_n in range(-1, 2):
                if row_n == 0 and col_n == 0:
                    continue
                possible_moves.append(Move((chr(ord(row) + row_n), int(col) + col_n)))
        self.nextmoves = possible_moves


class Knight(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Knight_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Knight_b.png")

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        for row_n in range(-1, 2):
            for col_n in range(-1, 2):
                #print(row_n, col_n)
                possible_moves.append((chr(ord(row) + row_n), int(col) + col_n))
        return possible_moves


class Rook(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Rook_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Rook_b.png")

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        for row_n in range(-1, 2):
            for col_n in range(-1, 2):
                #print(row_n, col_n)
                possible_moves.append((chr(ord(row) + row_n), int(col) + col_n))
        return possible_moves


class Bishop(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Bishop_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Bishop_b.png")

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        for row_n in range(-1, 2):
            for col_n in range(-1, 2):
                #print(row_n, col_n)
                possible_moves.append((chr(ord(row) + row_n), int(col) + col_n))
        return possible_moves


class Pawn(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Pawn_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Pawn_b.png")
        self.has_moved = False

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        if self.color  == "White":
            if col == "2":
                possible_moves.append(Move((chr(ord(row)), int(col)+1)))
                possible_moves.append(Move((chr(ord(row)), int(col)+2)))
            else:
                possible_moves.append(Move((chr(ord(row)), int(col)+1)))
        else:
            if col == "7":
                possible_moves.append(Move((chr(ord(row)), int(col)-1)))
                possible_moves.append(Move((chr(ord(row)), int(col)-2)))
            else:
                possible_moves.append(Move((chr(ord(row)), int(col)-1)))
        self.nextmoves = possible_moves


class Queen(Piece):
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        if color == "White":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Queen_w.png")
        elif color == "Black":
            self.image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Queen_b.png")

    def next_moves(self):
        possible_moves = list()
        row, col = self.position
        for row_n in range(-1, 2):
            for col_n in range(-1, 2):
                possible_moves.append((chr(ord(row) + row_n), int(col) + col_n))
        return possible_moves


class Board:
    scale_x = 73
    offset_x = 124
    scale_y = 73
    offset_y = 150

    def __init__(self):
        self.location = self.build_board()
        self.pieces =   [
                        King("E1", "White"), King("E8", "Black"),\
                        Queen("D1", "White"),Queen("D8", "Black"),\
                        Rook("A1", "White"),Rook("H1", "White"),Rook("A8", "Black"),Rook("H8", "Black"),\
                        Knight("B1", "White"),Knight("G1", "White"), Knight("B8", "Black"),Knight("G8", "Black"),\
                        Bishop("C1", "White"),Bishop("F1", "White"),Bishop("C8", "Black"),Bishop("F8", "Black"),\
                        Pawn("A2", "White"), Pawn("B2", "White"),Pawn("C2", "White"), Pawn("D2", "White"), Pawn("E2", "White"), Pawn("F2", "White"), Pawn("G2", "White"),Pawn("H2", "White"),\
                        Pawn("A7", "Black"), Pawn("B7", "Black"), Pawn("C7", "Black"), Pawn("D7", "Black"),Pawn("E7", "Black"), Pawn("F7", "Black"), Pawn("G7", "Black"), Pawn("H7", "Black"),
                        ]
        self.to_move = "White"
        self.checkmate = False
        self.board_image = pygame.image.load("C:\\users\\Steinshark\\PycharmProjects\\Chess_Game\\images\\Board.png")

    def build_board(self):
        new_list = list()
        for col in range(0,8):
            new_list.append(list())
            for row in range(0,8):
                new_list[col].append(chr(65+col)+ str(row+1))
        return new_list


g = Game()
g.play()
