import numpy as np
import matplotlib.pylab as plt
import pygame
import sys
import math

try:
    from tkinter import messagebox
except ImportError:
    from Tkinter import messagebox

# Global variables
DIM = 8

# Colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Screen Rendering Dimensions
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
width = DIM * SQUARE_SIZE
height = (DIM+1) * SQUARE_SIZE # additional empty row above
size = (width, height) #tuple

############################ INITIALISE VARIABLES #######################################
game_over = False
turn = 1
next_turn = 2
error = False
p1_score = 0
p2_score = 0
flip_num = 0
temp_pos_x = 0
temp_pos_y = 0

##################################### FUNCTIONS ##########################################

# Function to Initiate Board
def create_board():
    board = np.zeros((DIM,DIM))
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

# Function to check if player can place piece.
def can_play(board, piece):
    for r in range(DIM):
        for c in range(DIM):
            if is_vacant(board, r, c, piece):
                if is_reversible(board, r, c, piece):
                    return True
    return False

# Function to check if location is vacant.
def is_vacant(board, row, col, piece):
    # print("Check vacant")
    return board[row][col] == 0

# Determine if the placement of piece will lead to any reversals
def is_reversible(board, row, col, piece):
    # print("Determine Reversible")

    # Check right:
    if (col+1) <= DIM:
        # print(" determine right")
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
        # print(" determine left")
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
        # print(" determine up")
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
        # print(" determine down")
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
        # print(" determine +ve diagonal left")
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
                    # print("     location: row=", row_it, ", col=",c)
                    return True
            row_it = row_it + 1

    # Check positive diagonal, right of chess:
    if (col+1) <= DIM:
        row_it = row-1
        # print(" determine +ve diagonal right")
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
        # print(" determine -ve diagonal left")
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
        # print(" determine -ve diagonal right")
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
def drop_piece(board, row, col, piece):

    flip_num = 0

    # print("Drop piece and reverse")
    board[row][col] = piece

    # Variables
    reverse = False
    opp_row = row # identified row of the other chess
    opp_col = col # identified column of the other chess

    # Reverse pieces on the right:
    if (col+1) <= DIM:
        # print ("    check right", row, col)
        for c in range(col+1, DIM): # Start from the one to the right, not itself
            if board[row][c] == 0:
                break
            if board[row][c] == piece:
                reverse = True
                opp_col = c
                break
        if reverse == True:
            for c in range(col+1, opp_col):
                board[row][c] = piece
                flip_num = flip_num+1
                # print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse left (must check from right to left):
    if (col-1) >= 0:
        # print ("    check left", row, col)
        for c in range(col-1, 0, -1):
            if board[row][c] == 0:
                break
            if board[row][c] == piece:
                reverse = True
                opp_col = c
                break
        if reverse == True:
            for c in range(col-1, opp_col, -1):
                board[row][c] = piece
                flip_num = flip_num+1
                # print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse up (must check from down to up):
    if (row-1) >= 0:
        # print ("    check up", row, col)
        for r in range(row-1, 0, -1):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                reverse = True
                opp_row = r
                break
        if reverse == True:
            for r in range(row-1, opp_row, -1):
                board[r][col] = piece
                flip_num = flip_num+1
                # print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse down:
    if (row-1) <= DIM:
        # print ("    check down", row, col)
        for r in range(row+1, DIM):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                reverse = True
                opp_row = r
                break
        if reverse == True:
            for r in range(row+1, opp_row):
                board[r][col] = piece
                flip_num = flip_num+1
                # print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse positive diagonal, left of chess (going up to the right, so rows decreasing):
    if (col-1) >= 0:
        # print ("    check positive diagonal left", row, col)
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
                # print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False

    # Reverse positive diagonal, right of chess:
    if (col+1) <= DIM:
        # print ("    check positive diagonal right", row, col)
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
                # print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it - 1
        reverse = False

    # Reverse negative diagonal, left of chess:
    if (col-1) >= 0:
        # print ("    check negative diagonal left", row, col)
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
                # print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it - 1
        reverse = False

    # Reverse negative diagonal, right of chess:
    if (col+1) <= DIM:
        # print ("    check negative diagonal right", row, col)
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
                # print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False
    
    return flip_num

# Print board and scores
def print_board(board, flip_num): # 
    p1_score = np.count_nonzero(board==1)
    p2_score = np.count_nonzero(board==2)
    print("\nPlayer 1 pieces =", p1_score)
    print("Player 2 pieces =", p2_score)
    print("Number of flipped pieces: ", flip_num)
    print("Total number of pieces on the board: ", np.count_nonzero(board))
    print(board)
    # plt.imshow(board, cmap='hot', interpolation='nearest')
    # plt.show()

# End game (True if all entries are filled in)
def is_end_game(board):
    for c in range(DIM):
        for r in range(DIM): 
            if board[r][c] == 0:
                return False
    return True

# Draw Board (Graphics)
def draw_board(board):
    # Draw background
    for c in range(DIM):
        for r in range(DIM):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[r][c] == 1: # Player 1
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2: # Player 2
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            else:
                pass
    pygame.display.update() 

#################################### MAIN LOOP ###########################################

board = create_board()
print_board(board, 0)

#pygame variables
pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
myfont = pygame.font.SysFont("calibri",40)

# While loop for entire game
while not game_over:

    # Reinitialise Flags
    error = False

    # Blit Statistics
    if turn == 2:
        player_label = myfont.render(("Player 2"), 1, RED)
    else:
        player_label = myfont.render(("Player 1"), 1, YELLOW)
    screen.blit(player_label, (20,SQUARE_SIZE/2)) #only updates specific part of screen
    draw_board(board)

    # Main game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            print("turn =", turn)

            pygame.draw.rect(screen, BLACK, (0,0,width, SQUARE_SIZE))

            pos_x = event.pos[0] # Zeroeth element is horizontal axis, first element is vertical axis
            pos_y = event.pos[1]

            if can_play(board, turn):
                # Ask for Player input
                u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                u_col = int(math.floor(pos_x/SQUARE_SIZE))

                # Check for valid location and drop piece
                if is_vacant(board, u_row, u_col, turn) and is_reversible(board, u_row, u_col, turn):
                    flip_num = drop_piece(board, u_row, u_col, turn)
                else:
                    error = True
                    messagebox.showerror("Error", f"Position not valid. Player {turn} go again." % locals())

                # Check for end game
                if is_end_game(board):
                    print("End Game. Who wins?")
                    if (p2_score > p1_score):
                        print("Player 1 wins!")
                        messagebox.showinfo("Congrats!", "Player 1 won!")
                    elif (p2_score == p1_score):
                        print("It's a tie! You're both winners/ losers!")
                        messagebox.showinfo("Lol!", "It's a tie!")
                    else:
                        print("Player 2 wins!")
                        messagebox.showinfo("Congrats!", "Player 2 won!")
                    game_over = True

                # Print board
                p1_score = np.count_nonzero(board==1)
                p2_score = np.count_nonzero(board==2)
                stats_label = myfont.render((f"Total={np.count_nonzero(board)}, P1={p1_score}, P2={p2_score}, Flipped={flip_num}"), 1, WHITE)
                screen.blit(stats_label, (width-600,SQUARE_SIZE/2))
                print_board(board, flip_num)
                draw_board(board)
            else:
                messagebox.showerror("Can't Move!", f"Player {turn} cannot move. It is {next_turn}'s turn." % locals())
           
            # Next Player
            if error == False:
                if turn == 1:
                    turn = 2
                    next_turn =1
                else:
                    turn = 1
                    next_turn =2