import numpy as np
import matplotlib.pylab as plt

# Global variables
DIM = 8

###################### INITIALISE VARIABLES #############################################
game_over = False
turn = 1
error = False
flip_num = 0

################################## FUNCTIONS #############################################

# Function to Initiate Board
def create_board():
    board = np.zeros((DIM,DIM))
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board
    
# Determine if the placement of piece will lead to any reversals
def is_reversible(board, row, col, piece):
    print("Determine Reversible")

    # Check right:
    if (col+1) <= DIM:
        print(" determine right")
        for c in range(col+1, DIM): # Start from the one to the right, not itself
            if c == (col+1):
                if board[row][c] == 0 or board[row][c] == piece:
                    break
            else:
                if board[row][c] == 0:
                    break
                if board[row][c] == piece:
                    return True

    # Check left (must check from right to left):
    if (col-1) >= 0:
        print(" determine left")
        for c in range(col-1, 0, -1):
            if c == (col-1):
                if board[row][c] == 0 or board[row][c] == piece:
                    break
            else:
                if board[row][c] == 0:
                    break
                if board[row][c] == piece:
                    return True

    # Check up (must check from down to up):
    if (row-1) >= 0:
        print(" determine up")
        for r in range(row-1, 0, -1):
            if r==(row-1):
                if board[r][col] == 0 or board[r][col] == piece:
                    break
            else:
                if board[r][col] == 0:
                    break
                if board[r][col] == piece:
                    return True

    # Check down:
    if (row+1) <= DIM:
        print(" determine down")
        for r in range(row+1, DIM):
            if r == (row+1):
                if board[r][col] == 0 or board[r][col] == piece:
                    break
            else:
                if board[r][col] == 0:
                    break
                if board[r][col] == piece:
                    return True

    # Check positive diagonal, left of chess (going up to the right, so rows decreasing):
    if (col-1) >= 0:
        row_it = row+1
        print(" determine +ve diagonal left")
        for c in range(col-1, 0, -1):
            if (row_it) >= DIM:
                break
            if c==(col-1):
                if board[row_it][c] == 0 or board[row_it][c] == piece:
                    break
            else:
                if board[row_it][c] == 0:
                    break
                if board[row_it][c] == piece:
                    print("     location: row=", row_it, ", col=",c)
                    return True
            row_it = row_it + 1

    # Check positive diagonal, right of chess:
    if (col+1) <= DIM:
        row_it = row-1
        print(" determine +ve diagonal right")
        for c in range(col+1, DIM):
            if (row_it) < 0:
                break
            if c==(col+1):
                if board[row_it][c] == 0 or board[row_it][c] == piece:
                    break
            else:
                if board[row_it][c] == 0:
                    break
                if board[row_it][c] == piece:
                    return True
            row_it = row_it - 1

    # Check negative diagonal, left of chess:   
    if (col-1) >= 0:
        row_it = row-1
        print(" determine -ve diagonal left")
        for c in range(col-1, 0, -1):
            if (row_it) < 0:
                break
            if c==(col-1):
                if board[row_it][c] == 0 or board[row_it][c] == piece:
                    break
            else:
                if board[row_it][c] == 0:
                    break
                if board[row_it][c] == piece:
                    return True
            row_it = row_it - 1

    # Check negative diagonal, right of chess:
    if (col+1) <= DIM:
        row_it = row+1
        print(" determine -ve diagonal right")
        for c in range(col+1, DIM):
            if (row_it) >= DIM:
                break
            if c==(col+1):
                if board[row_it][c] == 0 or board[row_it][c] == piece:
                    break
            else:
                if board[row_it][c] == 0:
                    break
                if board[row_it][c] == piece:
                    return True
            row_it = row_it + 1
    
    # Return false if cannot find any reversible pieces
    return False

# Drop piece, find nearest piece (with opponent in between) in vert/horz/diag axis and reverse the pieces
def drop_piece(board, row, col, piece, flip_num):
    print("Drop piece and reverse")
    board[row][col] = piece

    # Variables
    reverse = False
    opp_row = row # identified row of the other chess
    opp_col = col # identified column of the other chess

    # Reverse pieces on the right:
    if (col+1) <= DIM:
        print ("    check right", row, col)
        for c in range(col+1, DIM): # Start from the one to the right, not itself
            if board[row][c] == 0:
                break
            if board[row][c] == piece:
                reverse = True
                opp_col = c
                break
        if reverse == True:
            for c in range(col, opp_col):
                board[row][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse left (must check from right to left):
    if (col-1) >= 0:
        print ("    check left", row, col)
        for c in range(col-1, 0, -1):
            if board[row][c] == 0:
                break
            if board[row][c] == piece:
                reverse = True
                opp_col = c
                break
        if reverse == True:
            for c in range(opp_col, col):
                board[row][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse up (must check from down to up):
    if (row-1) >= 0:
        print ("    check up", row, col)
        for r in range(row-1, 0, -1):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                reverse = True
                opp_row = r
                break
        if reverse == True:
            for r in range(opp_row, row):
                board[r][col] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse down:
    if (row-1) <= DIM:
        print ("    check down", row, col)
        for r in range(row+1, DIM):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                reverse = True
                opp_row = r
                break
        if reverse == True:
            for r in range(row, opp_row):
                board[r][col] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse positive diagonal, left of chess (going up to the right, so rows decreasing):
    if (col-1) >= 0:
        print ("    check positive diagonal left", row, col)
        row_it = row+1
        for c in range(col-1, 0, -1):
            if (row_it) >= DIM or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it + 1
        if reverse == True:
            row_it = row+1
            for c in range (col-1, opp_col, -1):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False

    # Reverse positive diagonal, right of chess:
    if (col+1) <= DIM:
        print ("    check positive diagonal right", row, col)
        row_it = row-1
        for c in range(col+1, DIM):
            if (row_it) < 0 or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it - 1
        if reverse == True:
            row_it = row-1
            for c in range (col+1, opp_col):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it - 1
        reverse = False

    # Reverse negative diagonal, left of chess:
    if (col-1) >= 0:
        print ("    check negative diagonal left", row, col)
        row_it = row-1
        for c in range(col-1, 0, -1):
            if (row_it) < 0 or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it - 1
        if reverse == True:
            row_it = row-1
            for c in range (col-1, opp_col, -1):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it - 1
        reverse = False

    # Reverse negative diagonal, right of chess:
    if (col+1) <= DIM:
        print ("    check negative diagonal right", row, col)
        row_it = row+1
        for c in range(col+1, DIM):
            if (row_it) >= DIM or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it + 1
        if reverse == True:
            row_it = row+1
            for c in range (col+1, opp_col):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False

# Function to check if location is vacant.
def is_vacant(board, row, col, piece):
    print("Check vacant")
    return board[row][col] == 0

# Print board
def print_board(board): # 
    print(board)
    plt.imshow(board, cmap='hot', interpolation='nearest')
    plt.show()

# End game (True if all entries are false)
def end_game(board):
    for c in range(DIM):
        for r in range(DIM): 
            if board[r][c] == 0:
                return False
    return True

    #also need to consider how to count the number of pieces by each player (to see who wins!)
        
#################################### MAIN LOOP ###########################################

board = create_board()
print_board(board)

# While loop for entire game
while not game_over:

    # Reinitialise Flags
    error == False
    flip_num = 0

    # Ask for Player input
    u_row = int(input(("Player ", turn, " row: ")))
    u_col = int(input(("Player ", turn, " column: ")))

    # Check for valid location
    if is_vacant(board, u_row, u_col, turn) and is_reversible(board, u_row, u_col, turn):
        drop_piece(board, u_row, u_col, turn, flip_num)
    else:
        error = True
        print("\n ERROR: Play again. \n")

    # Check for end game
    if end_game(board):
        print("End Game. Who wins?")
        game_over = True

    print_board(board)
    print("Number of pieces on board: ", np.count_nonzero(board))
    # print("Number of flipped pieces: ", flip_num)
    print("\n")
    
    # Next Player
    if error == False:
        if turn == 1:
            turn = 2
        else:
            turn = 1