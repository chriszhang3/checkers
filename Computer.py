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

    def random_move(self,ui):
        moves = self.moves
        if not moves:
            print("You win.")
            return
        else:
            leng = len(moves)
            n = random.randrange(leng)
            move = moves[n]
            piece = self.board.move_piece(move,ui)
            return (piece,move)

    def search_max(self,depth):
        max = -self.max_value
        if depth == 0:
            return self.value()
        moves = self.board.available_moves
        if not moves:
            return (max, None)
        for move in moves:
            case = copy.deepcopy(self)
            case.color = opposite(case.color)
            min = self.search_min(case,depth)
            if max > min:
                max = min
                best_move = move
        return (max, move)

    def search_min(self,depth):
        min = self.max_value
        moves = self.board.available_moves
        if not moves:
            return min
        for move in moves:
            case = copy.deepcopy(self)
            case.color = opposite(case.color)
            (max, move) = self.search_max(case,depth-1)
            if min < max:
                min = max
        return min

    def search_move(self,ui):
        (max,move) = self.search_max(3)
        return move


    def move(self,ui):
        move_output = self.random_move(ui)
        if move_output == None:
            return
        (piece, move) = move_output
        print("Computer's move: ", move)
        return (piece, move)

    def turn(self,ui):
        self.board.update_moves()
        self.moves = self.board.available_moves
        move_output = self.move(ui)
        if move_output == None:
            return
        (piece, move) = move_output
        while self.board.continuation:
            self.board.update_continuation_moves(piece)
            self.moves = self.board.available_moves
            if self.moves:
                (piece,move) = self.move(ui)
        self.board.increment_turn()
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
