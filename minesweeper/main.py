from tkinter import *
import random
import platform
from tkinter import messagebox

from .config import read, write

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.grid()
        self.wm_title("Minesweeper")
        self.iconbitmap("Assets/_flag.ico")
        self.assets = {
            "mine": PhotoImage(file="Assets/mine.png"),
            "fd": PhotoImage(file="Assets/facingDown.png"),
            "flagged": PhotoImage(file="Assets/flagged.png"),
        }
        for i in range(0, 6):
            self.assets[i] = PhotoImage(file=f"Assets/{i}.png")

        self.button_data = {}
        
        self.X = 25
        self.Y = 25
        
        self.btn_click = "<Button-1>"
        self.btn_flag = "<Button-2>" if platform.system() == "Darwin" else "<Button-3>"

        self.game_ended = False

        self.setup()

        # -- menu bar setup --
        self.menu = Menu(self)
        gamemenu = Menu(self.menu, tearoff=0)
        gamemenu.add_command(label="Easy (9x9 - 81 tiles)")
        gamemenu.add_command(label="Medium (16x16 - 256 tiles)")
        gamemenu.add_command(label="Hard (25x25 - 625 tiles)")
        self.menu.add_cascade(label="Difficulty", menu=gamemenu)
        self.configure(menu=self.menu)

    
    def _run(self):
        """
        Initiates the Tkinter window.
        """
        print("Minesweeper by acatia#5378!")
        self.mainloop()


    def mine_value(self, val):
        """
        An algorithm to determine whether a
        specific tile has any neighbour tiles
        that is a mine. If so, increment count
        by 1 and repeat for all tiles surrounding
        the target tile.

        It handles the KeyError exception because
        in the instance we are checking a tile that
        is out of the size of the grid, it will raise
        a KeyError.
        """
        count = 0
        val2 = val.split("_")

        x = int(val2[0])
        y = int(val2[1])

        board = self.button_data

        try: # Too lazy to use a loop so only 1 try-except will be needed but this will do for now
            if board[f"{x}_{y+1}"]["isMine"] == True: # Above middle
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x-1}_{y+1}"]["isMine"] == True:  # Above left
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x+1}_{y+1}"]["isMine"] == True:  # Above right
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x-1}_{y}"]["isMine"] == True:  # Middle left
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x+1}_{y}"]["isMine"] == True:  # Middle right
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x-1}_{y-1}"]["isMine"] == True:  # Bottom left
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x}_{y-1}"]["isMine"] == True:  # Bottom middle
                count += 1
        except KeyError:
            pass
        try:
            if board[f"{x+1}_{y-1}"]["isMine"] == True:  # Bottom right
                count += 1
        except KeyError:
            pass

        return count

    def setup(self):        
        """
        Generates a "new" board or loads it.
        
        Note that this will take some to generate
        lots of tiles. I recommend now loading more
        than 50x50 (2,500 tiles total) to prevent
        crashing it.
        """
        for x in range(self.X):
            for y in range(self.Y):
                randnum = random.randint(0, 100)

                if randnum <= 7:
                    isMine = True
                else:
                    isMine = False
                xy_coords = f"{x}_{y}"

                self.button_data[xy_coords] = {
                    "isMine": isMine,
                    "button": Button(self, image=self.assets["fd"], borderwidth=0, command=lambda xy_coords=xy_coords: self.reveal_tile(coords=xy_coords)),
                    "pos_x": x,
                    "pos_y": y,
                    "flagged": False
                }
                self.button_data[xy_coords]["button"].grid(row=x, column=y)
                self.button_data[xy_coords]["button"].bind(self.btn_flag, lambda event, coords=xy_coords: self.flag_tile(event, coords))

    def reveal_tile(self, coords):
        """Reveals the tile when it's been clicked on."""
        if self.game_ended:
            return
        if self.button_data[coords]["isMine"] == True: # It's a mine. kaboom
            self.button_data[coords]["button"].configure(image=self.assets["mine"])
            self.stop_game()
            return

        count = self.mine_value(coords)

        self.button_data[coords]["button"].configure(image=self.assets[count])
    
    def stop_game(self):
        """
        Stops the game either because a mine has
        been detonated, or they manually ended the 
        game.
        """
        # TODO: Stop timer
        self.game_ended = True
        messagebox.showwarning(
            title="Game Over",
            message="Oh no! You detonated a mine. Game over!"
        )
        self.reveal_mines()
        self.game_ended = False
        self.restart()
    
    def reveal_mines(self):
        """Shows all tiles once the game has ended."""
        for tile in self.button_data:
            if self.button_data[tile]["isMine"]:
                self.button_data[tile]["button"].configure(image=self.assets["mine"])
    
    def flag_tile(self, event, coords):
        """
        Called when a tile is right-clicked.
        This will put the flag icon on the tile.
        """
        print(coords)

        self.button_data[coords]["flagged"] = True
        self.button_data[coords]["button"].configure(image=self.assets["flagged"])

    def restart(self):
        for child in self.grid_slaves():
            child.grid_forget()
        
        self.setup()