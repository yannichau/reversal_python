import numpy as np

DIM = 8

################################## FUNCTIONS #############################################

# Function to Initiate Board
def create_board():
    board = np.zeros((DIM,DIM))
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

# Drop piece, find nearest piece in vertical/horizontal/diagonal axis and reversing the pieces
def drop_piece(board, row, col, piece):
    board[row][col] = piece

    # Variables
    reverse = False
    opp_row = row # identified row of the other chess
    opp_col = col # identified column of the other chess

    # Check right:
    for c in range(col+1, DIM): # Start from the one to the right, not itself
        if (col+1) >= DIM: # Break if start exceeds dimension
            break
        if board[row][c] == piece:
            reverse = True
            opp_col = c
            break
    if reverse == True:
        for c in range(col, opp_col):
            board[row][c] = piece
    reverse = False

    # Check left (must check from right to left):
    for c in range(col-1, 0, -1):
        if (col-1) <= 0:
            break
        if board[row][c] == piece:
            reverse = True
            opp_col = c
            break
    if reverse == True:
        for c in range(opp_col, col):
            board[row][c] = piece
    reverse = False

    # Check up (must check from down to up):
    for r in range(row-1, 0, -1):
        if (row-1) <= 0:
            break
        if board[r][col] == piece:
            reverse = True
            opp_row = r
            break
    if reverse == True:
        for r in range(opp_row, row):
            board[r][col] = piece
    reverse = False

    # Check down:
    for r in range(row+1, DIM):
        if (row-1) >= DIM:
            break
        if board[r][col] == piece:
            reverse = True
            opp_row = r
            break
    if reverse == True:
        for r in range(row, opp_row):
            board[r][col] = piece
    reverse = False

    # Check positive diagonal, left of chess (going up to the right, so rows decreasing):
    row_it = row+1
    for c in range(col-1, 0, -1):
        if (col-1) <= 0:
            break
        if board[row_it][c] == piece:
            reverse = True
            opp_row = row_it
            opp_col = c
            break
        row_it = row_it + 1
    if reverse == True:
        for c in range (opp_col, col):
            board[opp_row][opp_col] = piece
            opp_row = opp_row - 1
    reverse = False

    # Check positive diagonal, right of chess:
    row_it = row-1
    for c in range(col+1, DIM):
        if (col+1) >= DIM:
            break
        if board[row_it][c] == piece:
            reverse = True
            opp_row = row_it
            opp_col = c
            break
        row_it = row_it - 1
    if reverse == True:
        for c in range (col, opp_col):
            board[opp_row][opp_col] = piece
            opp_row = opp_row - 1
    reverse = False

    # Check negative diagonal, left of chess:
    row_it = row-1
    for c in range(col-1, 0, -1):
        if (col-1) <= 0:
            break
        if board[row_it][c] == piece:
            reverse = True
            opp_row = row_it
            opp_col = c
            break
        row_it = row_it - 1
    if reverse == True:
        for c in range (opp_col, col):
            board[opp_row][opp_col] = piece
            opp_row = opp_row + 1
    reverse = False

    # Check negative diagonal, right of chess:
    row_it = row+1
    for c in range(col+1, DIM):
        if (col+1) >= DIM:
            break
        if board[row_it][c] == piece:
            reverse = True
            opp_row = row_it
            opp_col = c
            break
        row_it = row_it + 1
    if reverse == True:
        for c in range (col, opp_col):
            board[opp_row][opp_col] = piece
            opp_row = opp_row + 1
    reverse = False

# Function to check if location is vacant.
def is_valid_location(board, row, col, piece):
    return board[row][col] == 0

# Print board
def print_board(board): # 
    print(board)

# End game (True if all entries are false)
def end_game(board):
    for c in range(DIM):
        for r in range(DIM): 
            if board[r][c] == 0:
                return False
    return True
        
#################################### MAIN LOOP ###########################################

# Initiate Variables
board = create_board()
print_board(board)
game_over = False
turn = 1

# While loop for entire game
while not game_over:
    # test = reverse(board, 1, 1, 1)
    pass