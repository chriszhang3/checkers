from Board import *
import random
from tkinter import *
import copy

def opposite(self,color):
    return (color+1)%2

class Computer:

    def __init__(self,board,color):
        self.board = board
        self.moves = []
        self.max_value = 24
        self.color = color

    def value(self):
        king_value = 2
        piece_value = 1
        color = self.color
        opp = opposite(color)
        total = 0
        for piece in self.board.pieces[color]:
            if piece.king:
                total += king_value
            else:
                total += piece_value
        for piece in self.board.pieces[opp]:
            if piece.king:
                total -= king_value
            else:
                total -= piece_value
        return total

    def random_move(self):
        moves = self.moves
        if not moves:
            print("You win.")
            return
        else:
            leng = len(moves)
            n = random.randrange(leng)
            move = moves[n]
            return move

    def search_max(self,depth):
        max = -self.max_value
        if depth == 0:
            return self.value()
        self.board.update_moves()
        moves = self.board.available_moves
        if not moves:
            return (max, None)
        for move in moves:
            case = copy.deepcopy(self)
            case.color = opposite(case.color)
            case.move_piece(move)
            min = self.search_min(case,depth)
            if max > min:
                max = min
                best_move = move
        return (max, best_move)

    def search_min(self,depth):
        min = self.max_value
        self.board.update_moves()
        moves = self.board.available_moves
        if not moves:
            return min
        for move in moves:
            case = copy.deepcopy(self)
            case.color = opposite(case.color)
            case.move_piece(move)
            max = self.search_max(case,depth-1)[0]
            if min < max:
                min = max
        return min

    def search_move(self,ui):
        (max,move) = self.search_max(10)
        if move == None:
            print("You win")
        return move

    def move(self,ui,move=None):
        if move == None:
            self.board.update_moves()
            self.moves = self.board.available_moves
            move = self.random_move()
        if move == None:
            return
        piece = self.board.move_piece(move,ui)
        return (piece, move)

    def turn(self,ui, move = None, log = False):
        move_output = move(ui,move)
        if move_output == None:
            return
        (piece, move) = move_output
        if log:
            print("Computer's move: ", move)
        while self.board.continuation:
            self.board.update_continuation_moves(piece)
            self.moves = self.board.available_moves
            if self.moves:
                (piece,move) = self.move(ui)
                if log:
                    print("Computer's move: ", move)
        self.board.increment_turn()
        if log:
            print("==========")
            print()
        return

def main():
    print("Execute main.py to play.")

    root = UI.start_tk()
    board = Board()
    computer = Computer(board,1)
    ui = UI.make_ui(board)
    canvas =ui.get_canvas()
    canvas.pack()

    canvas.bind('<Button-1>',
        lambda event, b=board, c= computer, u=ui: UI.onclick_computer(event,b,c,u))

    root.mainloop()
    return


if __name__ == "__main__":
    main()
