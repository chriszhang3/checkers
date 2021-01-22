from UI import *

class Piece:
    def __init__(self, color, king, y, x):

        # color is an integer. 0 is black and 1 is white
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

class Move:
    def __init__(self, ystart, xstart, ychange, xchange, eat):
        self.ystart= ystart
        self.xstart= xstart
        self.ychange= ychange
        self.xchange = xchange
        self.eat = eat
        if eat == False:
            self.yend = ystart + ychange
            self.xend = xstart + xchange
        else:
            self.yend = ystart + 2*ychange
            self.xend = xstart + 2*xchange

    def __str__(self):
        return "Move from (%d,%d) to (%d,%d)." % (ystart,xstart,yend,xend)

# If double jumping, don't need to click again

class Board:
    def __init__(self):
        self.board = []

        # Creates empty board
        row = []
        for i in range(8):
            row.append(None)
        for j in range(8):
            self.board.append(row.copy())

        self.available_moves = [] # Moves to be displayed.
        self.pieces = [[],[]]
        self.turn = 0
        self.can_move = False # You must click on a piece for this to become True.
        self.continuation = False # True if you are in the middle of a multi-jump.

        self.new_game()
        self.ui = self.make_ui()

    def make_ui(self):
        ui = UI()
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != None:
                    ui.place_piece(piece)
        return ui

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

    # Updates the possible moves of the piece and returns them.
    def possible_moves(self,piece):

        # print("Called possible_moves")

        if piece == None:
            return

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

                    # Final case is when the neighboring square is empty
                    else:
                        move = Move(y,x,y_change,x_change,False)
                        piece.moves.append(move)
            return piece.moves

    # Updates all moves of the player with designated color
    def update_moves(self,color):
        for piece in self.pieces[color]:
            self.possible_moves(piece)

    # Highlights all the possible moves a piece can make.
    def highlight_moves(self,piece):
        if piece == None:
            return []

        for move in piece.moves:
            if move.eat == True:
                color = "red"
            else:
                color = "yellow"
            self.ui.highlight(move.yend,move.xend, color)

        self.can_move = True
        return piece.moves

    def erase_highlighting(self):
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    piece = self.board[i][j]
                    if piece == None:
                        self.ui.remove_piece(i,j)
        return

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

    # Checks where the current play is able to eat any pieces.
    def can_eat(self):
        output = False
        for piece in self.pieces[self.turn]:
            for move in piece.moves:
                if move.eat == True:
                    output = True
        return output

    # Removes a piece from a specific tile. Doesn't remove it from the piece list.
    def remove_piece(self, y, x):
        self.board[y][x] = None
        self.ui.remove_piece(y,x)

    # Performs the move called move. Returns the piece if it ate another one.
    def move_piece(self, move):
        # print("Called move piece.")

        y = move.ystart
        x = move.xstart
        piece = self.board[y][x]
        y_new = move.yend
        x_new = move.xend
        eaten = None

        # Eats piece if appropriate
        if move.eat == True:
            # print(*self.pieces[0], sep= "\n")

            y_eaten = y + move.ychange
            x_eaten = x + move.xchange
            eaten_piece = self.board[y_eaten][x_eaten]

            self.pieces[eaten_piece.color].remove(eaten_piece)
            self.remove_piece(y_eaten,x_eaten)
            eaten = piece

        # If you reach the last row, make the piece a king.
        if y_new == piece.final:
            piece.king = True

        # Move Piece to new square.
        piece.y = y_new
        piece.x = x_new
        self.board[y_new][x_new] = piece
        self.ui.place_piece(piece)
        self.remove_piece(y,x)

        return eaten

    # Check if the piece can continue to eat.
    def after_eat(self, piece):
        moves = self.possible_moves(piece)
        continuation_moves = []
        for move in moves:
            if move.eat == True:
                continuation_moves.append(move)
                self.ui.highlight(move.yend,move.xend, "red")
        if continuation_moves:
            self.continuation = True
            self.available_moves = continuation_moves
            return
        else:
            self.continuation = False
            self.turn = (self.turn+1)%2
            
    # What happens when you click on the board
    def onclick(self,event):
        x = int(event.x/UI.cell_size)
        y = int(event.y/UI.cell_size)

        if self.continuation:
            for move in self.available_moves:
                if x == move.xend and y == move.yend:
                    self.erase_highlighting()
                    self.move_piece(move)
                    self.after_eat(self.board[y][x])

        else:

            # Click a piece to hightlight its possible moves
            if self.can_move == False:
                piece = self.board[y][x]
                if piece == None:
                    return
                elif piece.color != self.turn:
                    print("It is the turn of: %s" % UI.color_table[self.turn])
                    return
                else:
                    self.update_moves(self.turn)
                    self.available_moves = self.highlight_moves(piece)

                    # If there are not moves available, return to unhighlighted state.
                    if not self.available_moves:
                        self.can_move = False
                    return

            # If we are in a highlighted state, you can click where you want your piece to go.
            else:
                self.erase_highlighting()

                for move in self.available_moves:
                    if x == move.xend and y == move.yend:
                        if self.can_eat():
                            if move.eat == True:
                                eaten = self.move_piece(move)
                                if eaten != None:
                                    piece = self.board[y][x]
                                    self.after_eat(piece)

                            else:
                                print("If you can eat a piece this turn, you must.")
                        else:
                            self.move_piece(move)
                            self.turn = (self.turn+1)%2

                self.can_move = False
                return

def main():
    print("Execsute main.py to play.")
    return

if __name__ == "__main__":
    main()
