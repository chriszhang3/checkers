from Board import *
import random
from tkinter import *

class Computer:

    def __init__(self,board):
        self.board = board
        self.moves = []

    def random_move(self):
        moves = self.moves
        if not moves:
            print("You win.")
            return
        else:
            leng = len(moves)
            # print("length =", leng)
            n = random.randrange(leng)
            move = moves[n]
            piece = self.board.move_piece(move)
            return (piece,move)

    def search_max(self,depth):

        return

    def move(self):
        return self.random_move()

    def turn(self):
        self.board.update_moves()
        self.moves = self.board.available_moves
        if self.move() == None:
            return
        (piece, move) = self.move()
        while self.board.continuation:
            self.board.update_continuation_moves(piece)
            self.moves = self.board.available_moves
            if self.moves:
                (piece,move) = self.move()
        self.board.increment_turn()
        return

def main():
    print("Execute main.py to play.")

    root = UI.start_tk()
    board = Board()
    computer = Computer(board)
    ui = board.ui
    canvas =ui.get_canvas()
    canvas.pack()

    canvas.bind('<Button-1>',
        lambda event, b=board, c= computer: UI.onclick_computer(event,b,c))

    root.mainloop()
    return


if __name__ == "__main__":
    main()
