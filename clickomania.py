''' Eunha Koo
INF1340, Dr. Maher Elshakankiri
Midterm Project: Clickomania
Date created: 2021.11.12
Date last modified: 2021.11.18
'''

import tkinter as tk
from random import choice

class Game():
    WIDTH = 200 # width of the canvas
    HEIGHT = 320 # height of the canvas
    BOX_SIZE = 20 # width/height of each of the square boxes
    COLOURS = ("red", "yellow", "green", "blue", "purple") # colours of the boxes
    COLUMNS = 10 # number of columns of boxes
    ROWS = 16 # number of rows of boxes
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clickomania")
        self.root.geometry("300x500") # size of the window

        self.nav = tk.Frame(master=self.root, pady=5, padx=16) # top space in the window before the canvas is placed

        self.canvas = tk.Canvas(
            self.root,
            width=Game.WIDTH,
            height=Game.HEIGHT)
        self.matrix = [] # matrix will store the box ids and colours of each of the boxes, divided by columns
        self.column = [] # boxes in the columns will be placed from the bottommost to the topmost in this list
        self.deleted = [] # a list of the coordinates of the deleted boxes for each of the turns (will be initialized after every turn)
        x = 0 # this is the x_1 coordinate that will be incremented to place the boxes
        for column in range(Game.COLUMNS):
            y = Game.HEIGHT - Game.BOX_SIZE # this is the y_1 coordinate for the box
            for row in range(Game.ROWS):
                self.colour = choice(Game.COLOURS) # randomly choose a colour
                box = self.canvas.create_rectangle( 
                    x,
                    y,
                    x + Game.BOX_SIZE,
                    y + Game.BOX_SIZE,
                    fill=self.colour)
                y -= Game.BOX_SIZE # decrement y after each box is created to move 20 units up
                self.column.append((box, self.colour)) # append the box id and colour in a tuple to the self.column list
                self.canvas.tag_bind(box, "<Button-1>", self.popFirstBox) # bind each box with an event so that a function is called every time a box is clicked
            x += Game.BOX_SIZE # increment x after each column is done to move 20 units right
            self.matrix.append(self.column) # append the column list to the matrix
            self.column = [] # initialize the column list to start a new column
        
        self.footer = tk.Frame(master=self.root, pady=16, padx=16) # a footer to hold the reset button
        
        self.nav.pack(expand=True)
        self.canvas.pack(expand=True)
        self.footer.pack(expand=True)

        # create reset button
        btn_reset = tk.Button(
            master=self.footer,
            text="Reset",
            font=("Courier", 14),
            command=self.restartGame,
            padx=10,
            pady=3)

        btn_reset.pack()
            
        self.canvas.pack()

        
        
        self.root.mainloop() # create an event loop

    def restartGame(self):
        # remove the old canvas and the footer from the window to create new ones
        self.canvas.destroy()
        self.footer.destroy()        

        # create new canvas
        self.canvas = tk.Canvas(
            self.root,
            width=Game.WIDTH,
            height=Game.HEIGHT)
        self.matrix = []
        self.column = []
        self.deleted = []
        x = 0
        for column in range(Game.COLUMNS):
            y = Game.HEIGHT - Game.BOX_SIZE
            for row in range(Game.ROWS):
                self.colour = choice(Game.COLOURS)
                box = self.canvas.create_rectangle(
                    x,
                    y,
                    x + Game.BOX_SIZE,
                    y + Game.BOX_SIZE,
                    fill=self.colour)
                y -= Game.BOX_SIZE
                self.column.append((box, self.colour))
                self.canvas.tag_bind(box, "<Button-1>", self.popFirstBox)
            x += Game.BOX_SIZE
            self.matrix.append(self.column)
            self.column = []

        # create new footer with the reset button
        self.footer = tk.Frame(master=self.root, pady=16, padx=16)

        self.canvas.pack(expand=True)
        self.footer.pack(expand=True)

        btn_reset = tk.Button(
            master=self.footer,
            text="Reset",
            font=("Courier", 14),
            command=self.restartGame,
            padx=10,
            pady=3)

        btn_reset.pack()
            

    def popFirstBox(self, event):
        x = event.x # x coordinate of where the click happened
        y = event.y # y coordinate of where the click happened
        # find the box that was clicked in the canvas by using the enclosed area (20 units around the clicked area)
        box = self.canvas.find_enclosed(x-Game.BOX_SIZE,
                                        y-Game.BOX_SIZE,
                                        x+Game.BOX_SIZE,
                                        y+Game.BOX_SIZE)
        
        colour = self.canvas.itemcget(box, 'fill') # get colour of the clicked box

        # find the box that is directly above the cliced box
        box_up = self.canvas.find_enclosed(x-Game.BOX_SIZE,
                                        y- 2*Game.BOX_SIZE,
                                        x+Game.BOX_SIZE,
                                        y)
        # find the box that is directly below the cliced box
        box_down = self.canvas.find_enclosed(x-Game.BOX_SIZE,
                                        y,
                                        x+Game.BOX_SIZE,
                                        y+ 2*Game.BOX_SIZE)
        # find the box that is directly left of the cliced box
        box_left = self.canvas.find_enclosed(x- 2*Game.BOX_SIZE,
                                        y-Game.BOX_SIZE,
                                        x,
                                        y+Game.BOX_SIZE)
        # find the box that is directly right of the cliced box
        box_right = self.canvas.find_enclosed(x,
                                        y-Game.BOX_SIZE,
                                        x+ 2*Game.BOX_SIZE,
                                        y+Game.BOX_SIZE)

        # find colours of the surrounding boxes
        colour_up = self.canvas.itemcget(box_up, 'fill')
        colour_down = self.canvas.itemcget(box_down, 'fill')
        colour_left = self.canvas.itemcget(box_left, 'fill')
        colour_right = self.canvas.itemcget(box_right, 'fill')

        # get a boolean list checking whether the adjacent boxes match the clicked box's colour
        adjacents = [colour_up == colour,
             colour_down == colour,
             colour_left == colour,
             colour_right == colour]
        
        # if none of the colours match, return the function
        if adjacents == [False, False, False, False]:
            return
        
        else:
            if colour_up == colour: # if the box above has the same colour
                coords = (x, y - Game.BOX_SIZE) # get the x,y coordinates of a point inside the box above
                if coords not in self.deleted: # if the box is not already deleted in this turn
                    self.deleted.append(coords) # append to the deleted list
                self.deleteBox(box_up, x, y - Game.BOX_SIZE) # call the function to delete the box above
            if colour_down == colour: # same thing for all other sides
                coords = (x, y + Game.BOX_SIZE)
                if coords not in self.deleted:
                    self.deleted.append(coords)
                self.deleteBox(box_down, x, y + Game.BOX_SIZE)
            if colour_left == colour:
                coords = (x - Game.BOX_SIZE, y)
                if coords not in self.deleted:
                    self.deleted.append(coords)
                self.deleteBox(box_left, x - Game.BOX_SIZE, y)
            if colour_right == colour:
                coords = (x + Game.BOX_SIZE, y)
                if coords not in self.deleted:
                    self.deleted.append(coords)
                self.deleteBox(box_right, x + Game.BOX_SIZE, y)

        self.matrixDelete(self.matrix, box) # delete the current box from the matrix
        self.canvas.delete(box) # delete the current box from the canvas

        self.moveBox(self.deleted) # call function to move the boxes above the deleted boxes down
        
        self.checkEmptyColumn(self.matrix) # call function to check whether there is an empty column
                                           # when there is one, collapse that column so that every box to the right of that column moves one box space left
        self.checkGameResult(self.matrix) # check whether the user won or lost after every turn
        
        self.deleted = [] # initialize the deleted boxes list for the next turn

  

    def deleteBox(self, box, x, y):
        colour = self.canvas.itemcget(box, 'fill') # get the colour of the box being deleted
        self.matrixDelete(self.matrix, box) # delete the box from the matrix
        self.canvas.delete(box) # delete the box from the canvas

        # find the box above the deleted box and get its colour
        box_up = self.canvas.find_enclosed(x-Game.BOX_SIZE,
                                        y- 2*Game.BOX_SIZE,
                                        x+Game.BOX_SIZE,
                                        y)
        colour_up = self.canvas.itemcget(box_up, 'fill')
        if box_up and colour_up == colour: # if the colour is the same as the deleted box
            coords = (x, y - Game.BOX_SIZE) # get the coordinates of a point inside the box above 
            if coords not in self.deleted: # if the box is not already deleted
                self.deleted.append(coords) # append to the deleted list
            self.deleteBox(box_up, x, y - Game.BOX_SIZE) # call this function again recursively to check the same thing for the box above this box
        # same thing for the box below, left, and right of the box being deleted
        box_down = self.canvas.find_enclosed(x-Game.BOX_SIZE,
                                        y,
                                        x+Game.BOX_SIZE,
                                        y+ 2*Game.BOX_SIZE)
        colour_down = self.canvas.itemcget(box_down, 'fill')
        if box_down and colour_down == colour:
            coords = (x, y + Game.BOX_SIZE)
            if coords not in self.deleted:
                self.deleted.append(coords)
            self.deleteBox(box_down, x, y + Game.BOX_SIZE)

        box_left = self.canvas.find_enclosed(x- 2*Game.BOX_SIZE,
                                        y-Game.BOX_SIZE,
                                        x,
                                        y+Game.BOX_SIZE)
        colour_left = self.canvas.itemcget(box_left, 'fill')
        if box_left and colour_left == colour:
            coords = (x - Game.BOX_SIZE, y)
            if coords not in self.deleted:
                self.deleted.append(coords)
            self.deleteBox(box_left, x - Game.BOX_SIZE, y)

        box_right = self.canvas.find_enclosed(x,
                                        y-Game.BOX_SIZE,
                                        x+ 2*Game.BOX_SIZE,
                                        y+Game.BOX_SIZE)
        colour_right = self.canvas.itemcget(box_right, 'fill')
        if box_right and colour_right == colour:
            coords = (x + Game.BOX_SIZE, y)
            if coords not in self.deleted:
                self.deleted.append(coords)
            self.deleteBox(box_right, x + Game.BOX_SIZE, y)

    def matrixDelete(self, matrix, box):
        for i in range(len(matrix)): # for column in matrix
            for j in range(len(matrix[i])): # for row in column
                if [matrix[i][j][0]] == list(box): # if the id of the box in the matrix is the same as the box being deleted
                    del matrix[i][j] # delete that box from the matrix
                    return
                    

    def moveBox(self, deleted):
        # create a dictionary of the columns in order to sort the coordinates of the deleted boxes of the turn
        cols = {'col1':[],
                     'col2':[],
                     'col3':[],
                     'col4':[],
                     'col5':[],
                     'col6':[],
                     'col7':[],
                     'col8':[],
                     'col9':[],
                     'col10':[],
                     }
        # for the x,y coordinates in the deleted list
        for coord in deleted:
            if 0 < coord[0] < 20: # if the x coordinate is between 0 and 20
                cols['col1'].append(coord) # append to column 1 key
            elif 20 < coord[0] < 40: # if the x coordinate is between 20 and 40
                cols['col2'].append(coord) # append to column 2 key, etc.
            elif 40 < coord[0] < 60:
                cols['col3'].append(coord)
            elif 60 < coord[0] < 80:
                cols['col4'].append(coord)
            elif 80 < coord[0] < 100:
                cols['col5'].append(coord)
            elif 100 < coord[0] < 120:
                cols['col6'].append(coord)
            elif 120 < coord[0] < 140:
                cols['col7'].append(coord)
            elif 140 < coord[0] < 160:
                cols['col8'].append(coord)
            elif 160 < coord[0] < 180:
                cols['col9'].append(coord)
            elif 180 < coord[0] < 200:
                cols['col10'].append(coord)

        for key in cols: # for the list of deleted box coordinates in each of the columns
            cols[key] = sorted(cols[key], key=lambda x: x[1], reverse=True) # sort the items in the list so that the item with the highest y coord is in the front of the list (highest -> lowest)
            dists = [] # create a list of distances between the deleted boxes of the column
            if cols[key]: # if the column has a deleted box from the turn
                for i in range(len(cols[key])-1): # for each of the deleted box in the column
                    dist = (cols[key][i][1] - cols[key][i+1][1]) // 20 # get the distance between that box and the box above it that is deleted in the row (dist=1 means the box is directly above)
                    dists.append(dist) # append to the list of the distances

                # this part of the code is for when there is a gap between the deleted boxes of the column
                # when the boxes are not all directly on top of each other, the undeleted boxes between the deleted boxes have to move a different amount
                # compared to the boxes above the topmost deleted box of the column
                # this code will deal with that
                if dists and not all(x == 1 for x in dists): # if there are at least two deleted boxes in the column and they are not all directly on top of each other
                    count = 1 # count the number of box heights that needs to currently be moved
                    turn = 0 # track the number of times we move when there are more than one boxes between two deleted boxes
                    for dist in dists: # for distance in the distances list
                        if dist == 1: # if the distance between the two boxes are 1 (directly on top)
                            pass # no action needed
                        else: # if there is a gap between two boxes
                            while dist > 1: # while the distance is greater than 1
                                # find the box directly on top of the uppermost box of the two boxes currently being addressed
                                box_to_move = self.canvas.find_enclosed(cols[key][0][0] - Game.BOX_SIZE,
                                                    cols[key][0][1] - Game.BOX_SIZE - (count + turn) * Game.BOX_SIZE,
                                                    cols[key][0][0] + Game.BOX_SIZE,
                                                    cols[key][0][1] + Game.BOX_SIZE - (count + turn) * Game.BOX_SIZE)
                                self.canvas.move(box_to_move, 0, count * Game.BOX_SIZE) # move that box down 
                                dist -= 1 # decrement the distance now that the two boxes are one box height closer
                                turn += 1 # increment turn to find the correct box to move when there are more than one boxes between two deleted boxes
                                          # because count does not increment here and we need to find the next box which was directly on top of the box that was just moved one space down
                        count += 1 # now the next set of boxes need to be moved one box height more
                        
                # this is the first box to move that is on top of all the boxes with the gaps
                # this box and above will all be moving the same units down
                first_to_move = self.canvas.find_enclosed(cols[key][-1][0] - Game.BOX_SIZE,
                                                    cols[key][-1][1] - 2*Game.BOX_SIZE,
                                                    cols[key][-1][0] + Game.BOX_SIZE,
                                                    cols[key][-1][1])
                if first_to_move: # if the box above the uppermost deleted box exists
                    x_coor = cols[key][-1][0] # get the x coordinate of the topmost deleted box
                    y_coor = cols[key][-1][1] # get the y coordinate of the topmost deleted box
                    dist = len(cols[key]) * Game.BOX_SIZE # get the unit distance that the boxes need to be moved
                    while y_coor > 0: # while the distance between the y coordinate of the topmost box that was deleted/moved and the top of the canvas is greater than 0
                        # find the box that needs to be moved next
                        box_to_move = self.canvas.find_enclosed(x_coor - Game.BOX_SIZE,
                                            y_coor - 2*Game.BOX_SIZE,
                                            x_coor + Game.BOX_SIZE,
                                            y_coor)
                        self.canvas.move(box_to_move, 0, dist) # move the box the amount of distance we found
                        y_coor -= Game.BOX_SIZE # decrement y coordinate to move one box space above
                

    def checkEmptyColumn(self, matrix):
        cols_to_check = len(matrix) # the number of columns left to check
        curr_col = 0 # index of current column
        while cols_to_check > 0: # while there are columns to check
            if matrix[curr_col] == []: # if the current column is empty
                x1 = (curr_col+1) * Game.BOX_SIZE # find the x_1 coordinate of the total area of boxes right of the empty column that needs to be moved
                to_move = self.canvas.find_enclosed(x1-10, -10, Game.WIDTH+10, Game.HEIGHT+10) # using the x coordinate, get a list of all of the boxes that needs to be moved
                for box in to_move:
                    self.canvas.move(box, -Game.BOX_SIZE, 0) # move every box 20 units left
                del matrix[curr_col] # delete the empty column from the matrix
                cols_to_check -= 1 # decrement the number of columns left to check
            else:
                curr_col += 1 # if current column is not empty, move to the next column
            cols_to_check -= 1 # decrement the number of columns left to check

    def checkGameResult(self, matrix):
        # if matrix is empty, display a message that the user won
        if not matrix:
            lbl_won = tk.Label(
                master=self.canvas,
                text="You WON!",
                font=("courier", 14)
            )
            lbl_won.pack()
        # otherwise, check the colur of the bottom and left boxes of each of the boxes
        # this way, every side of every box will be checked without the index going out of range
        else:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if j != 0: # if the current box is not the bottommost box of the column (there is a box below this box)
                        if self.checkBottomColour(matrix, i, j): # call the function to compare the colour of the current box and the box directly below
                            return # if they are the same colour, return because the game is not over yet
                    elif i != 0 and len(matrix[i-1]) >= j: # if there is a box left to the current box
                        if self.checkLeftColour(matrix, i, j): # call the function to compare the colour of the current box and the box directly left
                            return # if they are the same colour, return because the game is not over yet
                    else:
                        pass # otherwise, move to the next box
            # if all the boxes left in the matrix has no adjacent boxes with the same colour, the game is over
            # display a message that the user lost
            lbl_lost = tk.Label(
                master=self.canvas,
                text="You Lost, try again!",
                font=("Courier", 14),
            )
            lbl_lost.pack()


    def checkBottomColour(self, matrix, i, j):
        return matrix[i][j][1] == matrix[i][j-1][1] # compare the colour of the current box and the box directly below

    def checkLeftColour(self, matrix, i, j):
        return matrix[i][j][1] == matrix[i-1][j][1] # compare the colour of the current box and the box directly left             
                                        


if __name__ == "__main__":
    game = Game() # create GUI



