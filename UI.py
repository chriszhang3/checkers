from tkinter import *
from Board import *

class UI(Frame): # Need to figure out what Frame is
    window_size = 608
    cell_size = int(window_size/8)
    color_table = ["black","white"]

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, bg="white", height=self.window_size, width=self.window_size)
        self.blank_board()

    # Make a blank board
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

    # Removes a piece at the cell specified
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

    # Highlights the cell specified
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

    # Places the specified piece on the cell specified
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
    print("Execute main.py to play.")

    root = Tk()
    root.geometry('250x150')

    button1 = Button(text="Left")
    button1.pack(side = LEFT)

    button2 = Button(text="Top")
    button2.pack(side = TOP)

    button3 = Button(text="Right")
    button3.pack(side = RIGHT)

    button4 = Button(text="Bottom")
    button4.pack(side = BOTTOM)

    root.mainloop()
    return

if __name__ == '__main__':
    main()
