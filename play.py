from tkinter import *
import random

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.grid()
        self.wm_title("Minesweeper")
        
        self.assets = {
            "mine": PhotoImage(file="Assets/mine.png"),
            "fd": PhotoImage(file="Assets/facingDown.png"),
            "flagged": PhotoImage(file="Assets/flagged.png"),
        }
        for i in range(0, 6):
            self.assets[i] = PhotoImage(file=f"Assets/{i}.png")

        self.button_data = {}
        
        self.X = 10
        self.Y = 10
        
        self.setup()

    
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

                if randnum <= 10:
                    isMine = True
                else:
                    isMine = False

                btn = Button(self, image=self.assets["fd"], borderwidth=0)
                btn.grid(row=x, column=y)

                self.button_data[f"{x}_{y}"] = {
                    "isMine": isMine,
                    "button": btn,
                    "pos_x": x,
                    "pos_y": y
                }
        
        for i in self.button_data:
            if self.button_data[i]["isMine"]:
                self.button_data[i]["button"].configure(image=self.assets["mine"])
            else:
                for k, v in self.button_data.items():
                    if v["isMine"]:
                        continue
                    val = self.mine_value(k)
                    print(val)
                    v["button"].configure(image=self.assets[val])
                    

Window()._run()
