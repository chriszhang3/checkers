from UI import *

class Piece:
    # color is an integer. 0 is black and 1 is white
    def __init__(self, color, king, y, x):

        self.color = color
        self.king = king
        self.y = y
        self.x = x
        self.moves = []

        if color == 1:
            self.left = 1
            self.forward = 1
            self.final = 7
        if color == 0:
            self.left = -1
            self.forward = -1
            self.final = 0

    def __str__(self):
        if self.king == True:
            name = "King"
        else:
            name = "Piece"
        return name+" of color \'%s\' in square (%d,%d)" % (UI.color_table[self.color],self.y,self.x)

class Move: # change a move to the old move
    def __init__(self, ystart, xstart, ychange, xchange, eat):
        self.ystart= ystart
        self.xstart= xstart
        self.ychange= ychange
        self.xchange = xchange

        # self.eat is a boolean telling whether this move is an eating move
        self.eat = eat
        if eat == False:
            self.yend = self.ystart + ychange
            self.xend = self.xstart + xchange
        else:
            self.yend = self.ystart + 2*ychange
            self.xend = self.xstart + 2*xchange

    def __str__(self):
        return "Move from (%d,%d) to (%d,%d)." % (self.ystart,
                                                self.xstart,
                                                self.yend,
                                                self.xend)

    @staticmethod
    def print_movelist(moves):
        print("{")
        for moves in moves:
            print(move)
        print("}")
        return

class Turn:
    def __init__(self, move = None):
        if move == None:
            self.moves = []
        else:
            self.moves = [move]

    def append(self, move):
        self.moves.append(move)

    def insert(self, move):
        self.moves.insert(0,move)

    def extend(self, turn):
        self.moves.extend(turn.moves)

    def get_last_move(self):
        if not self.moves:
            return None
        return self.moves[-1]

    def execute(self,board,ui=None, log = False):
        for move in self.moves:
            board.move_piece(move,ui)
            if log:
                print(move)
        board.continuation = False

    def is_empty(self):
        return self.moves==[]

    def __str__(self):
        output = "{\n"
        for move in self.moves:
            output = output + str(move) +",\n"
        output = output + "}\n"
        return output

class Board:
    def __init__(self):
        self.board = []

        # Creates empty board
        row = []
        for i in range(8):
            row.append(None)
        for j in range(8):
            self.board.append(row.copy())

        self.can_eat = False
        self.clicked_piece = None

        # self.pieces[0] are the pieces of player 0
        self.pieces = [[],[]]

        # The game starts with player 0's turn.
        self.turn = 0

        self.continuation = False # True if you are in the middle of a multi-jump.

        self.new_game()

    def new_game(self):
        for i in range(8):
            for j in range(8):
                if i < 3:
                    if (i+j)%2 == 0:
                        piece = Piece(1,False,i,j)
                        self.board[i][j] = piece
                        self.pieces[piece.color].append(piece)
                elif i >= 5:
                    if (i+j)%2 == 0:
                        piece = Piece(0,False,i,j)
                        self.board[i][j] = piece
                        self.pieces[piece.color].append(piece)
        return

    ### Methods related to possible moves ###

    # Updates the possible moves of the piece and returns them.
    def possible_moves(self,piece):

        if piece == None:
            return []

        else:
            y = piece.y
            x = piece.x
            y_sign_list = [1]
            if piece.king == True:
                y_sign_list.append(-1)

            piece.moves = []

            for y_sign in y_sign_list:
                for x_sign in [-1,1]:
                    y_change = y_sign*piece.forward
                    x_change = x_sign*piece.left
                    y_new = y+y_change
                    x_new = x+x_change

                    if not self.is_on_board(y_new,x_new):
                        continue
                    new_piece = self.board[y_new][x_new]
                    if self.is_same_color(new_piece, piece.color):
                        continue

                    # If the neighboring square has the opponent's piece,
                    # check if you can eat it
                    if self.is_opp_color(new_piece, piece.color):
                        y_new = y_new + y_change
                        x_new = x_new + x_change

                        if not self.is_on_board(y_new,x_new):
                            continue
                        if not self.is_empty(y_new,x_new):
                            continue

                        move = Move(y,x,y_change,x_change,True)
                        piece.moves.append(move)
                        self.can_eat = True

                    # Final case is when the neighboring square is empty
                    else:
                        move = Move(y,x,y_change,x_change,False)
                        piece.moves.append(move)
            return piece.moves

    # Updates all moves of the player and returns them
    def all_possible_moves(self):
        all_possible = []
        self.can_eat = False
        for piece in self.pieces[self.turn]:
            all_possible.extend(self.possible_moves(piece))

        if self.can_eat:
            old_moves = all_possible.copy()
            for move in old_moves:
                if move.eat == False:
                    all_possible.remove(move)
        return all_possible

    # A continuation move is when a piece eats two or more pieces in a row.
    # Returns a list of all possible continuation moves. Updates the value
    # of self.continuation

    def update_continuation_moves(self, piece, ui = None):

        move_list=[]
        self.possible_moves(piece)
        self.can_eat = False
        for move in piece.moves:
            if move.eat:
                self.can_eat = True
                move_list.append(move)
                if ui != None:
                    ui.highlight(move.yend,move.xend, "red")
        if not self.can_eat:
            self.continuation = False
        return move_list

    # Returns a list of turns of all possible continuations of a given turn.
    def all_continuation_seq(self, turn):
        turn_list = []
        last_move = turn.get_last_move()
        piece = self.board[last_move.yend][last_move.xend]
        # print(self)
        # print("Last move:", last_move)

        # All the moves in move_list should be eating moves
        move_list = self.update_continuation_moves(piece)

        if not move_list:
            turn_list.append(turn)
        else:
            for move in move_list:
                next_turn = copy.deepcopy(turn)
                next_turn.append(move)
                board = copy.deepcopy(self)
                board.move_piece(move)
                possible_turns = board.all_continuation_seq(next_turn)
                turn_list.extend(possible_turns)
        return turn_list

    def all_possible_turns(self):
        # print("Called all_possible_turns")
        turn_list = []
        moves = self.all_possible_moves()
        for move in moves:
            next_turn = Turn(move)
            if not move.eat:
                # print("Loc 3")
                turn_list.append(next_turn)
            else:
                next_move = copy.deepcopy(move)
                board = copy.deepcopy(self)
                board.move_piece(next_move)
                turn_list.extend(board.all_continuation_seq(next_turn))
        # print(*turn_list,sep="\n")
        # print("All possible turns exits")
        return turn_list

    # Highlights the given move.
    def highlight_moves(self,moves,ui):
        for move in moves:
            if move != None:
                if move.eat:
                    color = "red"
                else:
                    color = "yellow"
                ui.highlight(move.yend,move.xend, color)
        return

    def erase_highlighting(self, ui):
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    piece = self.board[i][j]
                    if piece == None:
                        ui.remove_piece(i,j)
        return

    ### Simple methods ###

    def is_on_board(self, y_new,x_new):
        if y_new < 0 or y_new >=8:
            return False
        if x_new < 0 or x_new >=8:
            return False
        return True

    def is_same_color(self, piece, color):
        if piece == None:
            return False
        else:
            return piece.color == color

    def is_opp_color(self, piece, color):
        if piece == None:
            return False
        else:
            return piece.color != color

    def is_empty(self, y_new, x_new):
        if self.board[y_new][x_new]==None:
            return True
        else:
            return False

    def increment_turn(self):
        self.turn = (self.turn+1)%2
        # self.continuation = False
        # print("==========")
        # print()
        return

    ### Methods that change the board state

    # Removes a piece from a specific tile. Doesn't remove it from the piece list.
    def remove_piece(self, y, x, ui = None):
        self.board[y][x] = None
        if ui != None:
            ui.remove_piece(y,x)

    # Performs the move called move. Returns the piece that moved.
    def move_piece(self, move, ui = None):
        # print("Called move piece.")

        if move == None:
            print("Can't execute the move None.")
            return

        y = move.ystart
        x = move.xstart
        piece = self.board[y][x]
        y_new = move.yend
        x_new = move.xend

        # Eats piece if appropriate
        if move.eat == True:

            y_eaten = y + move.ychange
            x_eaten = x + move.xchange
            eaten_piece = self.board[y_eaten][x_eaten]

            self.pieces[eaten_piece.color].remove(eaten_piece)
            if ui != None:
                self.remove_piece(y_eaten,x_eaten,ui)
            else:
                self.remove_piece(y_eaten,x_eaten)
            self.continuation = True

        # If you reach the last row, make the piece a king.
        if y_new == piece.final:
            piece.king = True

        # Move Piece to new square.
        piece.y = y_new
        piece.x = x_new
        self.board[y_new][x_new] = piece

        # print(piece)

        if ui != None:
            ui.place_piece(piece)
            self.remove_piece(y,x,ui=ui)
        else:
            self.remove_piece(y,x)

        return piece

    # What happens when you click on the board
    def human_turn(self,y,x, ui):

        # The case when you are in a continuation sequence
        if self.continuation:
            piece = self.clicked_piece
            self.possible_moves(piece)
            for move in piece.moves:
                if x == move.xend and y == move.yend:
                    self.erase_highlighting(ui)
                    piece = self.move_piece(move,ui)
                    self.update_continuation_moves(piece, ui=ui)
                    if self.continuation == False:
                        self.increment_turn()
                        self.clicked_piece = None

        else:

            # Click a piece to hightlight its possible moves
            # self.all_possible_turns()
            # print(self.continuation)
            if self.clicked_piece == None:
                piece = self.board[y][x]
                if piece == None:
                    return
                elif piece.color != self.turn:
                    print("It is the turn of: %s" % UI.color_table[self.turn])
                    return
                else:
                    # print("Loc 2")
                    self.all_possible_moves()
                    self.clicked_piece = piece
                    # print(piece)
                    moves = piece.moves
                    # print(*moves)
                    self.highlight_moves(moves,ui)
                    return

            # If we are in a highlighted state, you can click where you want your piece to go.
            else:
                self.erase_highlighting(ui)
                # print("Loc 1")
                moves = self.clicked_piece.moves
                for move in moves:
                    if x == move.xend and y == move.yend:
                        if self.can_eat:
                            if move.eat == True:
                                piece = self.move_piece(move,ui)
                                self.update_continuation_moves(piece, ui=ui)
                                if self.continuation == False:
                                    self.increment_turn()

                                # If you land here, self.clicked_piece is not reset
                                else:
                                    return

                            else:
                                print("If you can eat a piece this turn, you must.")

                        else:
                            self.move_piece(move,ui)
                            self.increment_turn()
                self.clicked_piece = None
                return

    def __str__(self):
        output = ""
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == None:
                    output = output + ". "
                elif piece.king == True:
                    if piece.color == 0:
                        output = output+"B "
                    else:
                        output = output+"W "
                else:
                    if piece.color == 0:
                        output = output+"b "
                    else:
                        output = output+"w "
            output = output+"\n"
        return output

def main():
    print("Execsute main.py to play.")
    print()
    return

if __name__ == "__main__":
    main()
