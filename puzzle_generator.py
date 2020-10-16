import random, sys
import pygame as pg
from pygame import mixer


pg.init()

# Creating the screen (x, y)
screen = pg.display.set_mode((700, 600))
# Loading the image into the my_image variable
my_image = pg.image.load('blank-sudoku-grid.png')


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
class Node:
    """Creating a node class to keep track of branching factor in the puzzle generatation"""

    def __init__(self):
        self.branching_factor = 0


def print_board(board_use):
    """Function that prints out the entire board array neatly."""
    # Loops through each line in the sudoku board
    for i in range(len(board_use)):
        # If the current row is a multiple of 3 and isn't the first line then print dashes to seperate the rows.
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - - - ')
        # Loop through each number in the row
        for j in range(len(grid[0])):
            # If the current number in the row is a multiple of 3 print a vertical dash without a new character.
            if j % 3 == 0:
                print(' | ', end='')
            # If it is the last number in the row print it.
            if j == 8:
                print(grid[i][j])
            # Otherwise print the number but with a space at the end, without a new character at the end.
            else:
                print(f"{grid[i][j]} ", end='')


def number_in_grid(n):
    """Takes in a potential number n to place on the board and returns how many there are on the board."""
    count_n = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == n:
                count_n += 1

    return count_n


def find_empty(board):
    """Finds the next empty square in the row and from a starting square."""
    # Loops through each element in the row, if it doesn't find an empty square it will return the next empty square
    # in the next row
    # Loops through each row
    for i in range(len(board)):
        # Loops through each number in the row
        for j in range(len(board[0])):
            # If the square at the current position we are in is 0, then return the position (j, i)
            # We are denoting empty squares on the board with a 0.
            if board[i][j] == 0:
                return (i, j)  # (row, col) (y, x)
    return False  # If the board is filled then it returns False, otherwise it will be True


def is_possible(y, x, num, board):
    """Takes in a tuple which is unpacked into the row and conlumn, and takes in the board as an argument, it then
    checks whether or not that number in the square is possible in that position. If that number can go in the position
    then it will return True otherwise it will return false"""
    # First check is to check weather or not that number can go in that certain place in the grid.
    # Rows in the board which belong to that grid
    for row in board[(y // 3) * 3: (y // 3) * 3 + 3]:
        # Columns in the current row we are in
        for column in row[(x // 3) * 3: (x // 3) * 3 + 3]:
            # If that current number we are on is that number we want to place it will return False.
            if column == num:
                return False
    # Second check to check if it can go into that row. Which is that number in the y coordinate.
    # Loops through each number in the current row that we are in which is given
    for column in board[y]:
        if column == num:  # If that number is the same as the number we are checking then return False
            return False
    # Last check to see if that number is repeated in the same column, which is the x coordinate.
    for row in board:  # Since the matrix containing the board is composed of rows, we can just loop through the list.
        if row[x] == num:  # If the number in the column is the same as the one we are checking return False
            return False
    return True  # If nothing returned False then it can be placed in that spot


num_count = 0

def fill_board1(board):
    """Functions that finds an empty square"""
    # global num_count
    # We are looping through the number 1 to 10.
    # for n in sorted(list(range(1, 10)), key= lambda r: number_in_grid(r)):
    for n in range(1, 10):
        # If the position where the empty number is can hold that number n, then it will set it to n.
        if is_possible(*(find_empty(board)), n, board):
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting that empty square to 0
            board[y][x] = n
            fill_board(board)
            board[y][x] = 0

def fill_board(board):
    """Functions that finds an empty square"""
    # We are looping through the number 1 to 10.
    # for n in sorted(list(range(1, 10)), key= lambda r: number_in_grid(r)):
    # List of random numbers which the function will loop through
    list_rands = random.sample(range(1, 10), 9)
    # Loops through the random list, finding a number which will fit, otherwise it will backtrack.
    for n in list_rands:
        # If the position where the empty number is can hold that number n, then it will set it to n.
        if is_possible(*(find_empty(board)), n, board):
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting that empty square to 0
            grid[y][x] = n
            fill_board(board)
            grid[y][x] = 0


def fill_9(board):
    global grid
    """Fills in the first 9 random squares on the board."""
    nums, ys, xs = random.sample(range(1, 10), 9), random.sample(
        range(9), 9), random.sample(range(9), 9)
    i = 0
    while i < 9:
        # Chooses a random number to put in, and random coordinates
        num = nums.pop()
        y = ys.pop()
        x = xs.pop()
        print(x, y)
        board[y][x] = num
        i += 1

#
# def fill_rest():
#     """Function that will fill in the rest of the board after the first 9 have been filled"""
#     global grid


def puzzle_maker(difficulty):
    """Function that randomly sets squares on the board to 0, and the number of squares depends on the difficulty
    you set as a argument for the function"""
    # Copied the grid that we generated the solution for
    grid_return = grid[:]
    # A list of 81 numbers from 0 - 80, randomly shuffled. Will be used to get y and x coordinates.
    nums_81 = random.sample(range(81), 81)
    # Setting n many squares to 0, where n is the difficulty parameter
    for dif in range(difficulty):
        # Setting the y and x positions, where y is random number after integer dividing it by 9, leaving the row
        # number, the x coordinate is the remainder after diving the random number by 9.
        num = nums_81.pop(5)
        y, x = num // 9, num % 9
        # Setting that random square to 0
        grid_return[y][x] = 0
    return grid_return


def difficulty_score(nodes):
    """Function that quantifies the difficulty of the puzzle into a score"""
    # Looping through each nodes in the nodes list
    branch_difficulty_score = 0
    for node in nodes:
        branches = node.branching_factor
        print(branches)
        # print((branches - 1)**2)
        if branches != 0:
            branch_difficulty_score += (branches - 1)**2
    return branch_difficulty_score


# List of nodes with branching factors
list_nodes = []


def branch_factor(board, node):
    global list_nodes
    """Functions that finds an empty square"""
    # We are looping through the number 1 to 10.
    # for n in sorted(list(range(1, 10)), key= lambda r: number_in_grid(r)):
    # List of random numbers which the function will loop through
    list_rands = random.sample(range(1, 10), 9)
    # Loops through the random list, finding a number which will fit, otherwise it will backtrack.
    for n in list_rands:
        # If the position where the empty number is can hold that number n, then it will set it to n.
        if is_possible(*(find_empty(board)), n, board):
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting that empty square to 0
            grid[y][x] = n
            # When a possible square value is found it will add to the branching factor in the current node
            node.branching_factor += 1
            # Creating a node to be used
            node1 = Node()
            list_nodes.append(node1)
            branch_factor(board, node1)
            grid[y][x] = 0


def final_puzzle():
    root_node = Node()
    list_nodes.append(root_node)
    num_clues = 30
    new_grid = puzzle_maker(num_clues)
    try:
        branch_factor(new_grid, root_node)
    except TypeError:
        pass
    final_difficulty_score = (difficulty_score(
        list_nodes) * 100 + (81 - num_clues))
    return final_difficulty_score


def solution(board):
    """Prints the solution of the board"""
    # Since the find empty returns False when the board is filled it will raise a TypeError exception, we need to handle
    # it.

    try:
        fill_board(board)
    except TypeError:
        pass
    # print_board(board)
        


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


    def handle_event(self, event):
        """Function that handles the event that is occuring, changing the text in the square in different ways."""
        global grid
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
    
    def check_solution(self):
        """Uses the returned solved sudoku board to check if your current solution is valid or not"""
        global grid
        gridA = grid[:]     # Creating a copy of the grid we are using
        solution(gridA)     # Solves the copied board
        if grid == gridA:
            print("congrats")
        else:
            print('ya')

    def check_event(self, event):
        # Checking if the button was clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                global grid     # Solves the copied board
                if grid == gridA:
                    print("congrats")
                else:
                    print('ya')


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
    # try:
    #     fill_board1(gridA)
    # except TypeError:
    #     pass
    # fill_9(grid)
    # # Creating the root node to track of all the branching factors
    # solution(grid)
    # # difficulty_score(list_nodes)
    # print(final_puzzle())
    # Initiliaze pg

    # Creating the squares objects in the board and the border lines to block the grey lines
    squares = create_squares(grid)
    squaresx, squaresy = create_borders()

    running = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(my_image, (0, 0))

        # Drawing the squares on the board
        for row in squares:
            for square in row:
                square.draw(screen)

        check_solution_button = Button(600, 400, 80, 40, 4)
        check_solution_button.draw(screen)
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

                running = False
            for row in squares:
                for square in row:
                    square.handle_event(event)
            check_solution_button.check_event(event)
            # if event.type == 

        # Updates the display
        pg.display.update()

if __name__ == '__main__':
    main()


# Starting pg coding

# # Initiallzing pg
# pg.init()

# # Creating the screen (x, y)
# screen = pg.display.set_mode((800, 600))
