from tkinter import *
from Board import *

class UI(Frame):
    window_size = 640
    cell_size = int(window_size/8)
    color_table = ["black","white"]

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, bg="white", height=self.window_size, width=self.window_size)
        self.blank_board()

    def blank_board(self):
        self.master.title("checkers")
        self.pack(fill=BOTH, expand=1)

        for i in range (8):
            for j in range(8):
                if (i+j)%2==0:
                    self.canvas.create_rectangle(
                        0+self.cell_size*i,
                        0+self.cell_size*j,
                        self.cell_size+self.cell_size*i,
                        self.cell_size+self.cell_size*j,
                        outline="black",
                        fill="gray")

    def remove_piece(self,y,x):
        unit = self.cell_size
        if (y+x)%2==0:
            color = "gray"
        else:
            color = "white"
        self.canvas.create_rectangle(
            unit*x,
            unit*y,
            unit*x+unit,
            unit*y+unit,
            outline="black",
            fill=color)

    def highlight(self, y, x, color):
        # print("called highlight",y,x)

        unit = self.cell_size
        self.canvas.create_rectangle(
            unit*x,
            unit*y,
            unit*x+unit,
            unit*y+unit,
            outline = "black",
            fill=color)

    def place_piece(self,piece):
        unit = self.cell_size
        y = piece.y
        x = piece.x
        color = piece.color
        king = piece.king

        fill_color = UI.color_table[color]

        self.canvas.create_oval(
            unit*x+unit/8,
            unit*y+unit/8,
            unit*x+unit*7/8,
            unit*y+unit*7/8,
            outline="black",
            fill=fill_color)

        if king == True:
            self.canvas.create_oval(
                unit*x+unit/4,
                unit*y+unit/4,
                unit*x+unit*3/4,
                unit*y+unit*3/4,
                outline="gray",
                width=2)

    def get_canvas(self):
        return self.canvas


def main():

    root = Tk()
    window_size = UI.window_size
    root.geometry(str(window_size)+'x'+str(window_size))
    board = Board()
    ui = board.ui
    canvas =ui.get_canvas()
    canvas.pack()

    canvas.bind('<Button-1>', board.onclick)

    root.mainloop()







if __name__ == '__main__':
    main()
