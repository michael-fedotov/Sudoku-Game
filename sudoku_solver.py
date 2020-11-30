import random
import sys

# sample_grid, very difficult puzzle
sample_grid = [
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

def print_board(board_use):
    """Function that prints out the entire board array neatly."""
    # Loops through each line in the sudoku board
    for i in range(len(board_use)):
        # If the current row is a multiple of 3 and isn't the first line then print dashes to seperate the rows.
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - - - ')
        # Loop through each number in the row
        for j in range(len(board_use[0])):
            # If the current number in the row is a multiple of 3 print a vertical dash without a new character.
            if j % 3 == 0:
                print(' | ', end='')
            # If it is the last number in the row print it.
            if j == 8:
                print(board_use[i][j])
            # Otherwise print the number but with a space at the end, without a new character at the end.
            else:
                print(f"{board_use[i][j]} ", end='')

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

def fill_board(board):
    """Functions that finds an empty square"""
    # We are looping through the number 1 to 10.
    for n in range(1, 10):
        # If the position where the empty number is can hold that number n, then it will set it to n.
        if is_possible(*(find_empty(board)), n, board):
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting that empty square to 0
            board[y][x] = n
            fill_board(board)
            board[y][x] = 0


def random_fill_board(board):
    """Fills the board recursively with random values"""
    # Creating a randomly shuffled list of numbers from 1-9
    loop_nums = random.sample(list(range(1,10)), 9)
    
    # Looping through the main numbers
    for n in loop_nums:
        # If that number n can be placed in the empty square, then it will proceed recursively
        if is_possible(*(find_empty(board)), n, board):
            # Setting the y and x coordinate variable to the empty square coordinates
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting the square in the board equal to that number n
            board[y][x] = n

            # Going in the matrix, calling the function recursively, that it checks for the next empty square
            random_fill_board(board)

            # If the recursion stopped at some point then it will backtrack to the last point and 
            # continue the search for another n
            board[y][x] = 0

def fill_9(board):
    global grid1
    """Fills in the first 9 random squares on the board."""
    nums, ys, xs = random.sample(range(1, 10), 9), random.sample(
        range(9), 9), random.sample(range(9), 9)
    for i in range(9):
        # Chooses a random number to put in, and random coordinates
        num = nums.pop()
        y = ys.pop()
        x = xs.pop()
        board[y][x] = num

def solution(board):
    """Prints the solution of the board"""
    # Filling the first 9 squares randomly
    # fill_9(board)
    # Handling the error of when the board finishes solving it
    try:
        random_fill_board(board)
    except TypeError:
        pass
    print_board(board)
    return board




def empty_grid_gen():
    """Returns a filled board to the user"""
    # Empty board
    board = [
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
    # Filling the first 9 squares randomly
    fill_9(board)
    # Filling the rest of the board
    try:
        random_fill_board(board)
    except TypeError:
        pass
    return board