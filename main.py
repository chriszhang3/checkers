from tkinter import *
from Board import *
from UI import *

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





if __name__ == "__main__":
    main()
