from Board import *
import random
from tkinter import *
import copy
import time

def opposite(color):
    return (color+1)%2

class Computer:

    def __init__(self,board,color):
        self.max_value = 24

    def value(self,board,color):
        king_value = 2
        piece_value = 1
        opp = opposite(color)
        total = 0
        for piece in board.pieces[color]:
            if piece.king:
                total += king_value
            else:
                total += piece_value
        for piece in board.pieces[opp]:
            if piece.king:
                total -= king_value
            else:
                total -= piece_value
        return total


    ### SECTION
    ### The methods in this section implement a computer player that searches
    ### through various possible moves.

    def search_max(self, board, depth, color, move_list, alpha, beta):
        value = -self.max_value
        turn = Turn() # Figure out when I actually need to define this.
        best_move = None

        # If depth is zero, give the current board value.
        if depth == 0:
            value = self.value(board, color)
            # print(board)
            # print(value)
            return (value,turn)

        # If there are no moves, this means the turn is over. Switch to the other player.
        if not move_list:
            board.increment_turn()
            following_moves = board.all_possible_moves()
            output = self.search_max(board,
                                        depth-1,
                                        opposite(color),
                                        following_moves,
                                        -beta,
                                        -alpha)
            # print("Output",output[0],type(output[0]))
            output_value = -output[0]
            return (output_value,turn)

        # Check all possible moves.
        for move in move_list:
            case = copy.deepcopy(board)
            case.move_piece(move)

            if move.eat == True:
                piece = case.board[move.yend][move.xend]
                following_moves = case.update_continuation_moves(piece)
                (output_value,output_turn) = self.search_max(case,
                                            depth,
                                            color,
                                            following_moves,
                                            alpha,
                                            beta)

            else:
                case.increment_turn()
                following_moves = case.all_possible_moves()
                output = self.search_max(case,
                                            depth-1,
                                            opposite(color),
                                            following_moves,
                                            -beta,
                                            -alpha)
                # print("Output",output[0],type(output[0]))
                output_value = -output[0]
                output_turn = turn


            if output_value > value:
                value = output_value
                alpha = max(alpha,value)
                if alpha>beta:
                    return (self.max_value,None)
                best_move = move
                turn = output_turn

        if best_move != None:
            turn.insert(best_move)

        return (value,turn)

    def search_turn(self,board,ui):
        move_list = board.all_possible_moves()

        # second input should be even number
        start_time = time.time()
        (max,turn) = self.search_max(board,4,1,move_list,-self.max_value,self.max_value)
        print("max is", max)
        print(time.time()-start_time)
        if turn.is_empty():
            print("You win")
        else:
            turn.execute(board,ui,log=True)
        print("==========")
        print()
        board.increment_turn()

    ### The following methods implement a computer player who plays randomly.

    def random_move(self,board,move_list):
        if not move_list:
            print("You win.")
            return None
        else:
            leng = len(move_list)
            n = random.randrange(leng)
            move = move_list[n]
            return move

    def single_move(self,board,ui):
        move_list = board.all_possible_moves()
        move = self.random_move(board,move_list)
        if move == None:
            return
        piece = board.move_piece(move,ui)
        return move

    def turn(self,board,ui):
        move = self.single_move(board,ui)
        print("Computer's move: ", move)
        while board.continuation:
            piece = board.board[move.yend][move.xend]
            move_list = board.update_continuation_moves(piece)
            if move_list:
                move = self.single_move(ui)
                print("Computer's continuation move: ", move)
        board.increment_turn()
        print(board.continuation)
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
