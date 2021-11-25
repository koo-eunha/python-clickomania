# Clickomania

Clickomania (a variation is known as SameGame) is played on a grid of c columns and r rows (c=10 and r=16 in this game). 
The grid is initially filled with differently coloured square stones, comprising k colours (5 colours in this game). 
Groups are formed by stones of the same colour of which the edges are touching. A move deletes a group that contains 
at least two stones. Stones are continuously pulled downwards until they touch either the bottom of the grid or another stone, 
so that any gaps made by deleting a group are filled by any stones above it. 
When a column is deleted all of the stones to the left and right of it move together to fill the space.
A solution is successful if it removes every single stone.

Game description from https://www.researchgate.net/publication/220174445_A_Survey_of_NP-Complete_puzzles

# Instructions

Download the project, and open the "clickomania.py" file and start playing.

# Files
## clickomania.py
This is the file we will run to play the game.

# Examples

1. When you clear the puzzle, a message saying "You WON!" will be displayed.

2. When you lose the game (i.e., all the leftover blocks has no same colours adjacent to them),
   a message saying "You Lost, try again!" will be displayed.
   
At any point of the game, you can click on the "Reset" button on the bottom to start a new puzzle.
