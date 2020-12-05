
""" to do, 
import solution into board so it can update or check if you have a correct response
place board to display from generator function
button to generate new problems
check button
make sure each cell can only have one of each number?""" 

import random, sys
import pygame as pg
from pygame import mixer
import sudoku_solver


# from sudoku import solution as sol
# from sudoku import solution

# Move all functions to other
# Pull the version where the code worked in solutions and make it generate a puzzle
# from sudoku import main11

pg.init()

# Creating the screen (x, y)
screen = pg.display.set_mode((700, 600))
# Loading the image into the my_image variable
my_image = pg.image.load('blank-sudoku-grid.png')

# from sudoku import gridA
# Sample grid
grid1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

grid2 = [
    [0, 8, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 8, 4, 0, 9, 0],
    [0, 0, 6, 3, 2, 0, 0, 1, 0],
    [0, 9, 7, 0, 0, 0, 0, 8, 0],
    [8, 0, 0, 9, 0, 3, 0, 0, 2],
    [0, 1, 0, 0, 0, 0, 9, 5, 0],
    [0, 7, 0, 0, 4, 5, 8, 0, 0],
    [0, 3, 0, 7, 1, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 4, 0],
]

# Make this the generated sudoku puzzle
grid3 = sudoku_solver.solution(grid2)

# TODO Add a diffuculyy feature??? Where they chose after or at the
full_solved, grid_gen = sudoku_solver.puzzle_maker(0)
# print(full_solved)
# print("\n", grid_gen)


grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]


gridA = grid[:]







class Square:
    """Class that will represent a sudoku square and can be filled with a number"""
    
    def __init__(self, x, y, w, h, width, num="", isclue=False):
        self.rect = pg.Rect(x, y, w, h)

        # Color attribute, by default set to inactive
        self.color = (137, 137, 137)
        # When inactive the color will be border of the square
        self.color_inactive = (137, 137, 137)   # (137, 137, 137)
        # When the box is clicked it will change color until enter is pressed or another square is pressed
        self.color_active = (20, 20, 200)

        # Number that the user places in the square
        self.number = num

        # Font object, default set to inactive
        self.font = pg.font.Font(None, 32)
        # Font object for the text inside
        self.font_inactive = pg.font.Font(None, 32)
        # Font object when the text is active
        self.font_active = pg.font.Font(None, 50)

        # Text properties object, default set to inactive
        self.txt_surface = self.font_inactive.render(self.number, True, self.color)
        # Text properties for the text, when inactive
        self.txt_surface_inactive = self.font_inactive.render(self.number, True, self.color_inactive)
        # Text properties when active
        self.txt_surface_active = self.font_active.render(self.number, True, self.color_active)
        

        # Square will only be active if it is clicked upon
        self.active = False
        # Width when drawing the lines
        self.width = width

        # Coordinates of the square
        self.coords = None

        # Sets the attribute to wether or not the current square is a clue or not.
        self.clue = isclue

    def active_changer(self):
        """Function that changes attributes depending on if active is True or not."""
        # If active is True it will change all attributes to their active state
        if self.active:  
            self.color = self.color_active
            self.font = self.font_active
            self.txt_surface = self.txt_surface_active

        # Otherwise if inactive it will set it to inactive
        else:
            self.color = self.color_inactive
            self.font = self.font_inactive
            self.txt_surface = self.txt_surface_inactive


    def handle_event(self, event, grid):
        """Function that handles the event that is occuring, changing the text in the square in different ways."""
        # Checks if the event is the mouse being pressed down
        if event.type == pg.MOUSEBUTTONDOWN:
            # Checks to see if the rectangle was clicked, by checking if the position of the click falls in the 
            # parametres of the rectangle. The square must not be a clue for it to be changeable by the user.
            if self.rect.collidepoint(event.pos) and not self.clue:
                self.active = not self.active   # Setting it to the opposite of the current setting
                self.active_changer()    # Changes the instance attributes to their active states
            else:
                # If the mouse is clicked outside of the rectangle then the text is not active
                self.active = False
                self.active_changer()    # Sets the instance attributes to inactive
                # Renders the text in the inactive mode, making it set 
                self.txt_surface = self.font.render(self.number, True, self.color)

        
        # If the event is a key being pressed down
        if event.type == pg.KEYDOWN:
            # If the text box is active, or the rectangle has been clicked on 
            if self.active:
                # If the enter key has been pressed, stored in the event instance attribute key
                if event.key == pg.K_RETURN:
                    # If return is pressed then active is set to false, and the active changer changes it
                    self.active = False
                    self.active_changer()
                # If backspace is pressed clears the number
                elif event.key == pg.K_BACKSPACE:
                    """If backspace is pressed it clears the square"""
                    self.number = ""
                else:
                    # Checks if it is a nubmer if its not it will pass
                    try:
                        int(event.unicode)
                    except ValueError:
                        pass
                    else:
                        # If the number inputed is an integer, then it will th
                        if isinstance(int(event.unicode), int):
                            if event.unicode != "0":    # All numbers but 0, because sudoku is 1-9
                                self.number = event.unicode
                # Rendering the text
                # Only one digit numbers are printed, it is setting the number that is going to be printed 
                # to the keystroke in the events, so each new keystroke resets the current number to the new 
                # keystroke.
                self.txt_surface = self.font.render(self.number, True, self.color)
        if not self.clue:
            y = self.coords[0]
            x = self.coords[1]
            if self.number:
                grid[y][x] = int(self.number)
    def draw(self, screen):
        """Draws the number in the text box and the box itself"""
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, self.width)


class Button(Square):
    """Class that will represent button objects, like check solution or create new puzzle, 
    inherets from the square class so its functionality is similar."""
    def __init__(self, x, y, w, h, width, num="", isclue=False):
        # Using the inhereted classes init function to initialize the class attributes
        super().__init__(x, y, w, h, width, num="", isclue=False)

        # Text variable for the button
        self.txt_surface1 = (pg.font.Font(None, 30)).render("CHECK", True, (20, 20, 20))
        # TODO Next button is going to be a next level

    
    def check_solution(self):
        """Uses the returned solved sudoku board to check if your current solution is valid or not"""
        global full_solved
        global grid_gen
        # gridA = grid[:]     # Creating a copy of the grid we are using
        # sudoku_solver.solution(gridA)     # Solves the copied board
        # gridA = sudoku_solver.solution(grid2[:])
        if grid_gen == full_solved:
            print("congrats")
        else:
            print('ya')

    def check_event(self, event):
        global full_solved
        global grid_gen
        # Checking if the button was clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # global grid     # Solves the copied board
                # if grid == gridA:
                #     print("congrats")
                # else:
                #     print('ya')
                # gridA = grid[:]     # Creating a copy of the grid we are using
                # # gridtemp = sudoku_solver.solution(grid[:])     # Solves the copied board
                if grid_gen == full_solved:
                    print("congrats")
                else:
                    print('ya')

    def draw_button(self,screen ):
        """Draws the button onto the screen"""
        # Drawing the button and the text onto the screen
        screen.blit(self.txt_surface1, (self.rect.x+5, self.rect.y+12))
        pg.draw.rect(screen, (55, 55, 55), self.rect, self.width)
                # self.check_solution()


# def set_square_sudoku(squares, grid):
#     """Takes a list of square objects, and sets each ones number attribute to the numbers in the sudoku grid.
#     Each number that is not a zero will be set to each instances number attribute, where 0 is for the user 
#     to fill"""


def create_squares(grid):
    """Creates a list of row lists of squares. Each square will be a Square object with calculated dimensions
    and place to be plotted. Each square will have its number attribute set to the corresponding nubmer
    in the sudoku grid. All non-zero numbers will be immutable squares and the ones were the number attribute
    is 0 will be mutable by the user."""

    # Empty list of squares
    squares = []

    # Intial y value
    y = 4-55

    # Loops through 9 times for each column and 9 times for each row. 
    # Each times adding a square object to the list of squares.
    for i in range(9):
        y += 55
        x = 4-55
        squarestemp = []
        for j in range(9):
            x += 55
            sudoku_number = grid[i][j]

            # Adding the square object with the parametres calculated, wdith and height are standard
            # the number will be the corresponding number in the sudoku grid.
            if sudoku_number != 0:  # If the number is not 0 it will be added
                squarestemp.append(Square(x, y, 55, 55, 1, num=str(sudoku_number), isclue=True))
                
            else:   # If the number is 0, it will not be an argument.
                # Creating the square with the coordinates that it represents on the board
                square = Square(x, y, 55, 55, 1)
                square.coords = (i, j)
                # Adding the square to the list to be added
                squarestemp.append(square)    
        squares.append(squarestemp)

    return squares


def create_borders():
    """Function that returns a list of rectangles in form of lines so they can be drawn onto the borders of 
    the sudoku board"""

    # Initial x and y positions
    x1 = 4
    y1 = 4

    # List to store the borderline square objects
    squaresx = []
    squaresy = []

    # Loops 4 times as there are 4 major borders along the columns, each time adding a borderline to the list
    for i in range(4):
        square_to_add = Square(x1, 1, 1, 502, 4)
        # Changing the color of the object to 0, 0, 0
        square_to_add.color_inactive = (0, 0, 0)
        squaresx.append(square_to_add)
        x1 += 3 * 55

    # Loops through 4 times, there are 4 major row borders, each iteration adds a borderline to the list
    for i in range(4):
        square_to_add = Square(1, y1, 502, 1, 4)
        # Changing the color of the object to 0, 0, 0
        square_to_add.color_inactive = (0, 0, 0)
        squaresy.append(square_to_add)
        y1 += 3 * 55

    return squaresx, squaresy

def main():
    """Calls the necessary functions to generate the puzzle, then remove the squares according to difficulty."""
    # Creating the squares that will be used, loading the generated grid
    squares = create_squares(grid_gen)
    squaresx, squaresy = create_borders()



    running = True
    while running:
        # sudoku_solver.print_board(grid_gen)
        # print(grid_gen == full_solved)
        # Adding the background image
        screen.fill((255, 255, 255))
        screen.blit(my_image, (0, 0))

        # Drawing the squares on the board
        for row in squares:
            for square in row:
                square.draw(screen)

        # 
        check_solution_button = Button(550, 400, 80, 40, 4, num="Button")
        check_solution_button.draw_button(screen)
        # Drawing the lines on the boarders of the puzzle
        for square in squaresx:
            square.draw(screen)
        for square in squaresy:
            square.draw(screen)

        # Checks each of the events
        for event in pg.event.get():
            # If the event is the quit event then it will exit the program
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                # Exits the file
                running = False
            for row in squares:
                for square in row:
                    square.handle_event(event, grid_gen)
            check_solution_button.check_event(event)
            # if event.type == 

        # Updates the display
        pg.display.update()

if __name__ == '__main__':
    main()
