from tkinter import Tk

from main import Window

if __name__ == "__main__":
    root = Tk()
    root.wm_title("Minesweeper")
    root.geometry("500x500")

    app = Window(root)
    app.configure(bg="grey17")

    # Initialize the window
    root.mainloop()