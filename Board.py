from UI import *

class Piece:
    def __init__(self, color, king, y, x):

        # color is an integer. 0 is black and 1 is white
        self.color = color
        self.king = king
        self.y = y
        self.x = x

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

class Board:
    def __init__(self):
        self.board = []

        # Creates empty board
        row = []
        for i in range(8):
            row.append(None)
        for j in range(8):
            self.board.append(row.copy())

        self.can_move = False
        self.moves = []
        self.pieces = [[],[]]
        self.turn = 0

        self.new_game()
        self.ui = self.make_ui()

    def make_ui(self):
        ui = UI()
        for i in range(8):
            for j in range(8):
                type = self.board[i][j]
                if type != None:
                    ui.place_piece(i,j,type.color,type.king)
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

    def possible_moves(self,y,x):
        # print("Called possible_moves")

        moves = []
        piece = self.board[y][x]

        if piece == None:
            return moves
        else:
            y_sign_list = [1]
            if piece.king == True:
                y_sign_list.append(-1)

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

                    if self.is_opp_color(new_piece, piece.color):
                        y_new = y_new + y_change
                        x_new = x_new + x_change

                        if not self.is_on_board(y_new,x_new):
                            continue
                        if not self.can_eat(y_new,x_new):
                            continue

                        move = Move(y,x,y_change,x_change,True)
                        self.ui.highlight(y_new,x_new)
                        moves.append(move)

                    else:
                        move = Move(y,x,y_change,x_change,False)
                        self.ui.highlight(y_new,x_new)
                        moves.append(move)
            self.can_move = True
            return moves

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

    def can_eat(self, y_new, x_new):
        if self.board[y_new][x_new]==None:
            return True
        else:
            # print("Can't eat this way")

            return False

    def onclick(self,event):
        x = int(event.x/UI.cell_size)
        y = int(event.y/UI.cell_size)

        # Click a piece to hightlight its possible moves
        if self.can_move == False:
            self.moves = self.possible_moves(y,x)

            # If there are not moves available, return to unhighlighted state.
            if not self.moves:
                self.can_move = False
            return

        # If we are in a highlighted state, you can click where you want your piece to go.
        if self.can_move == True:
            self.erase_highlighting()
            for move in self.moves:
                if x == move.xend and y == move.yend:
                    # print("Location 1",x,y,move.xend,move.yend)

                    self.move_piece(move)
            self.can_move = False
            return

    # Removes a piece from a specific tile. Doesn't remove it from the piece list.
    def remove_piece(self, y, x):
        self.board[y][x] = None
        self.ui.remove_piece(y,x)


    def move_piece(self, move):
        y = move.ystart
        x = move.xstart
        piece = self.board[y][x]

        y_new = move.yend
        x_new = move.xend

        # Eats piece if appropriate
        if move.eat == True:
            # print(*self.pieces[0], sep= "\n")

            y_eaten = y + move.ychange
            x_eaten = x + move.xchange
            eaten_piece = self.board[y_eaten][x_eaten]
            
            self.pieces[eaten_piece.color].remove(eaten_piece)
            self.remove_piece(y_eaten,x_eaten)

        # Move Piece to new square. If you reach the last row, make the piece a king.
        if y_new == piece.final:
            piece.king = True

        piece.y = y_new
        piece.x = x_new
        self.board[y_new][x_new] = piece
        self.ui.place_piece(y_new,x_new,piece.color,piece.king)

        self.remove_piece(y,x)
        return

    # def __str__(self):
    #     output = ""
    #     for i in range(8):
    #         for j in range(8):
    #             cell = self.board[i][j]
    #             if cell == None:
    #                 output = output+". "
    #             else:
    #                 if cell.color == "black" and cell.king == False:
    #                     piece = "b"
    #                 elif cell.color == "black" and cell.king == True:
    #                     piece = "B"
    #                 elif cell.color == "white" and cell.king == False:
    #                     piece = "w"
    #                 elif cell.color == "white" and cell.king == True:
    #                     piece = "W"
    #                 output = output + piece + " "
    #         output = output + "\n"
    #     return output

def main():
    list1 = []
    list2 = []
    list = [list1,list2]
    list1.append(Piece(0,False,1,2))
    print(*list)


    # board = Board()
    # board.new_game()
    # print(board)
    #
    # while(True):
    #     # 0 is black, 1 is white
    #     print("Turn of "+str(board.turn))
    #     print("y coordinate of piece:")
    #     y = int(input())
    #     print("x coordinate of piece:")
    #     x = int(input())
    #     print("Where to move piece:")
    #     where = int(input())
    #     board.move(y,x,where)
    #     print(board)




if __name__ == "__main__":
    main()
