
""" to do,
import solution into board so it can update or check if you have a correct response
place board to display from generator function
button to generate new problems
check button
make sure each cell can only have one of each number?"""

import random
import sys
import time
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

# # Make this the generated sudoku puzzle
# grid3 = sudoku_solver.solution(grid2)

# Creating the variables for storing the sudoku boards.
full_solved = None
grid_gen = None

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
        self.txt_surface = self.font_inactive.render(
            self.number, True, self.color)
        # Text properties for the text, when inactive
        self.txt_surface_inactive = self.font_inactive.render(
            self.number, True, self.color_inactive)
        # Text properties when active
        self.txt_surface_active = self.font_active.render(
            self.number, True, self.color_active)

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
                self.txt_surface = self.font.render(
                    self.number, True, self.color)

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
                self.txt_surface = self.font.render(
                    self.number, True, self.color)
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
    def __init__(self, x, y, w, h, width, num=""):
        # Creating the rectangle object with user inputs
        self.rect = pg.Rect(x, y, w, h)
        
        # Storing the width and the height
        self.width = width
        self.height = h

        # Variable to determine if the text showing up is active.
        self.active = False


        # Setting up the fonts where when inactive it does not show up, it is initially inactive.
        self.font_inactive = pg.font.Font(None, 0)
        self.font_not_equal_active = pg.font.Font(None, 40)
        self.font_active = pg.font.Font(None, 40)

        self.text_not_match = "BOARD NOT SOLVED"
        self.text_match = "YOU HAVE SOLVED THE BOARD"
        self.text_new_game = "PRESS NEXT TO PLAY NEW PUZZLE"

        # # The variables used in the board
        # self.font_board_match = self.font_inactive
        # self.font_board_not_match = self.font_inactive

        # Text surface for the text when you have the correct board or the boards do not match.
        self.board_not_match_active = self.font_active.render(self.text_not_match, True, (20, 20, 20))
        self.board_match_active = self.font_active.render(self.text_match, True, (20, 20, 20))
        self.board_message_next = self.font_active.render(self.text_new_game, True, (20, 20, 20))

        
        # self.board_not_match_inactive = self.font_inactive.render(self.text_not_match, True, (20, 20, 20))
        # self.board_match_inactive = self.font_inactive.render(self.text_match, True, (20, 20, 20))


        # self.board_not_match = self.board_not_match_inactive
        # self.board_match = self.board_match_inactive

        # Text variable for the button with the font, letters and color.
        self.txt_surface1 = (pg.font.Font(None, 30)).render("CHECK", True, (20, 20, 20))
    
    
    
    # def active_changer1(self):   
    #     """Function that changes attributes depending on if active is True or not."""
    #     # If active is True it will change all attributes to their active state
    #     if self.active == 1:
    #         # self.color = self.color_active
    #         self.font_board_match = self.font_active
    #         self.board_match = self.board_match_active

    #     # Otherwise if inactive it will set it to inactive
    #     elif self.active == 2:
    #         # self.color = self.color_inactive
    #         self.font_board_not_match = self.font_active
    #         self.board_not_match = self.board_not_match_active

    #     else:
    #         # Changing them to the inactive font so that the don't show up.
    #         self.font_board_not_match = self.font_inactive
    #         self.board_match = self.board_match_active
    #         self.board_not_match = self.board_not_match_inactive


    
    
    # def check_solution(self):
    #     """Uses the returned solved sudoku board to check if your current solution is valid or not"""
    #     global full_solved
    #     global grid_gen
    #     # gridA = grid[:]     # Creating a copy of the grid we are using
    #     # sudoku_solver.solution(gridA)     # Solves the copied board
    #     # gridA = sudoku_solver.solution(grid2[:])
        
    #     # Always displaying the message until user presses enter.
    #     if grid_gen == full_solved:
    #         # Setting the active to True and calling the active changer function
    #         self.active = True
    #         active_changer()
    #     else:
    #         print('ya')

    
        
    
    def check_event(self, event):
        """Function that checks the events and if the mouse is clicked it will check if the fully solved board is the 
        same as the users board, if they are that means the user solved the board."""
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
                if full_solved == grid_gen:
                    # If the board is solved it will show the message for the board being solved, self.active = 1
                    # self.active = 1
                    # self.active_changer1()

                    # Displaying the text on the board for 3 seconds.
                    screen.blit(self.board_match_active, (50, 200))
                    screen.blit(self.board_message_next, (50, 300))
                    pg.display.update()
                    time.sleep(5)
                else:
                    # If the board is not solved it will show the appropriate message, self.active = 2
                    # self.active = 2
                    # self.active_changer1()

                    # Displaying the text on the screen for 3 seconds.
                    screen.blit(self.board_not_match_active, (200 , 200))
                    pg.display.update()
                    time.sleep(3)
                    # print('ya')
                    # screen.blit((pg.font.Font(None, 40)).render("PLEASE TRY AGAIN", True, (20, 20, 20)), (100, 100))

    def draw_button(self,screen ):
        """Draws the button onto the screen"""
        # Drawing the button and the text onto the screen
        screen.blit(self.txt_surface1, (self.rect.x+5, self.rect.y+12))
        pg.draw.rect(screen, (55, 55, 55), self.rect, self.width)
        
        # Drawing the text to show if the board do match or don't
        # screen.blit(self.board_not_match, (100 , 100))
        # screen.blit(self.board_match, (50, 50))
                # self.check_solution()


# def set_square_sudoku(squares, grid):
#     """Takes a list of square objects, and sets each ones number attribute to the numbers in the sudoku grid.
#     Each number that is not a zero will be set to each instances number attribute, where 0 is for the user 
#     to fill"""

class ButtonNextSolution:
    """Class that will represent a button that lets the user generate a new board."""
    def __init__(self, x, y, w, h, width, num=""):
        self.rect = pg.Rect(x, y, w, h)
        self.width = width
        self.height = h
        self.txt_surface2 = (pg.font.Font(None, 40)).render("NEW", True, (20, 20, 20))

    def check_event(self, event):
        """Checks the event in the main loop and if the button is pressed on 
        then it will create a new puzzle"""
        global full_solved
        global grid_gen
        # Checking if the button was clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # If the user clicked on to the next puzzle, it will return False breaking the loop, which will then 
                # break the while loop and generate another board.
                return False
        # If there was nothing clicked then return True, keep the loop going.
        return True

    def draw_button(self,screen ):
        """Draws the button onto the screen"""
        # Drawing the button and the text onto the screen
        screen.blit(self.txt_surface2, (self.rect.x+5, self.rect.y+12))
        pg.draw.rect(screen, (55, 55, 55), self.rect, self.width)
                # self.check_solution()


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

def main_loop():
    """Calls the necessary functions to generate the puzzle, then remove the squares according to difficulty."""
    # Making those 2 variables global so that we can use them in the main function.
    global full_solved, grid_gen
    # Choses a random difficuly by selecting a random number of squares to remove.
    # full_solved, grid_gen = sudoku_solver.puzzle_maker(random.randint(50,60))
    full_solved, grid_gen = sudoku_solver.puzzle_maker(0)


    
    # Creating the squares that will be used, loading the generated grid
    squares = create_squares(grid_gen)
    squaresx, squaresy = create_borders()

    # Creating the button that checks the solution.
    check_solution_button = Button(550, 400, 80, 40, 4, num="Button")

    new_puzzle_button = ButtonNextSolution(550, 300, 80, 40, 4, num = "BUTTON")

    

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

        # Drawing the check solution button to the screen.
        check_solution_button.draw_button(screen)
        new_puzzle_button.draw_button(screen)
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
            # If the button is clicked the loop will be broken and generating a new board
            running = new_puzzle_button.check_event(event)
            # check_solution_button.check_event(event,full_solved, grid_gen)

        # Updates the display in each loop
        pg.display.update()

def main():
    """Main loop"""
    # While the puzzle is running, 
    while True:
        main_loop()


if __name__ == '__main__':
    main()
