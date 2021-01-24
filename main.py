from tkinter import *
from Board import *
from UI import *

def main():

    root = Tk()
    board_size = UI.window_size
    cell_size = int(board_size/8)
    window_size = board_size+cell_size
    letters = ["A","B","C","D","E","F","G","H"]

    root.geometry(str(window_size)+'x'+str(window_size))

    board = Board()
    ui = board.ui
    canvas =ui.get_canvas()
    canvas.pack()
    canvas.place(x=0,y=0)
    canvas.bind('<Button-1>', board.onclick)


    for i in range(8):
        label = Label(root,
    		 text=letters[i],
    		 #fg = "light green",
    		 #bg = "dark green",
    		 font = "Helvetica %d"%int(cell_size/2))
        label.pack()
        label.place(x = cell_size*i+22, y = board_size+15)

    for number in range(8):
        label = Label(root,
             text=str(number+1),
             #fg = "light green",
             #bg = "dark green",
             font = "Helvetica %d"%int(cell_size/2))
        label.pack()
        label.place(x = board_size+27, y = 14+number*cell_size)


    root.mainloop()





if __name__ == "__main__":
    main()
