import random
# Sample grid
grid = [
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
    for row in board[(y // 3) * 3: (y // 3) * 3 + 3]:  # Rows in the board which belong to that grid
        for column in row[(x // 3) * 3: (x // 3) * 3 + 3]:  # Columns in the current row we are in
            if column == num:  # If that current number we are on is that number we want to place it will return False.
                return False
    # Second check to check if it can go into that row. Which is that number in the y coordinate.
    for column in board[y]:  # Loops through each number in the current row that we are in which is given
        if column == num:  # If that number is the same as the number we are checking then return False
            return False
    # Last check to see if that number is repeated in the same column, which is the x coordinate.
    for row in board:  # Since the matrix containing the board is composed of rows, we can just loop through the list.
        if row[x] == num:  # If the number in the column is the same as the one we are checking return False
            return False
    return True  # If nothing returned False then it can be placed in that spot


num_count = 0


def fill_board(board):
    """Functions that finds an empty square"""
    print(9)
    # We are looping through the number 1 to 10.
    # for n in sorted(list(range(1, 10)), key= lambda r: number_in_grid(r)):
    list_rands = random.sample(range(1, 10), 9)
    for n in list_rands:
        # If the position where the empty number is can hold that number n, then it will set it to n.
        if is_possible(*(find_empty(board)), n, board):
            y, x = find_empty(board)[0], find_empty(board)[1]
            # Setting that empty square to 0
            grid[y][x] = n
            fill_board(board)
            grid[y][x] = 0

def fill_9(board):
    """Fills in the first 9 random squares on the board."""
    nums, ys, xs = random.sample(range(1, 10), 9), random.sample(range(9), 9), random.sample(range(9), 9)
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


def solution(board):
    """Prints the solution of the board"""
    # Since the find empty returns False when the board is filled it will raise a TypeError exception, we need to handle
    # it.
    try:
        fill_board(board)
    except TypeError:
        pass
    print_board(board)

def puzzle_maker(difficulty):
    """Function that randomly sets squares on the board to 0, and the number of squares depends on the difficulty
    you set as a argument for the function"""
    nums_81 = random.sample(range(81), 81)
    for i in difficulty:
        for rand in nums_81:
            # Setting the y and x





fill_9(grid)
try:
    fill_board(grid)
except TypeError:
    pass

print_board(grid)