import numpy as np
# import matplotlib.pylab as plt
import pygame
from pygame.locals import *
import sys
import math
import random

# Global variables
DIM = 8
PLAYER = 1
AI = 2
EMPTY = 0

# Colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (36, 173, 66)
BROWN = (198, 135, 17)
GRAY = (128, 128, 128)

# Screen Rendering Dimensions
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
width = (DIM+6) * SQUARE_SIZE
height = (DIM+2) * SQUARE_SIZE # additional empty row above
size = (width, height) #tuple

# Player and Statistics Locations
stats_box_top_left = ((DIM+2)*SQUARE_SIZE, SQUARE_SIZE)
player_centre = (int((DIM+2)*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE*1.5)
stats_box_width = SQUARE_SIZE*3
stats_box_height = SQUARE_SIZE*DIM
stats_box_dim = (stats_box_width, stats_box_height)
stats_line1_centre = (int((DIM+2)*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE*3)
stats_line2_centre = (int((DIM+2)*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE*3.5)
stats_line3_centre = (int((DIM+2)*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE*4)
stats_line4_centre = (int((DIM+2)*SQUARE_SIZE+SQUARE_SIZE/2), SQUARE_SIZE*4.5)

################################## TEMPORARY VARIABLES #####################################
p1_score = 0
p2_score = 0
flip_num = 0
playable_list = []
wood_img = pygame.image.load('media/light_wood.jpg')

##################################### FUNCTIONS ##########################################

# Function to Initiate Board
def create_board():
    board = np.zeros((DIM,DIM))
    board[3][3] = 1
    board[4][4] = 1
    board[3][4] = 2
    board[4][3] = 2
    return board

# Initialise board of available playing locations, for either player.
def create_avaiBoard(turn):
    available_board = np.zeros((DIM,DIM))
    if turn == PLAYER:
        available_board[3][5] = 1
        available_board[5][3] = 1
        available_board[2][4] = 1
        available_board[4][2] = 1
    elif turn == AI:
        available_board[2][3] = 2
        available_board[3][2] = 2
        available_board[5][4] = 2
        available_board[4][5] = 2        
    return available_board

# Function to check if player can place piece.
def can_play(board, piece):
    # print("Can play?")
    for r in range(DIM):
        for c in range(DIM):
            if is_vacant(board, r, c, piece):
                if orthello(board, r, c, piece, False):
                    return True
    return False

# Function to return a list of available locations.
def availoc(board, available_board, piece):
    playable_locs = []
    # print("Return a list of playable locations.")
    for r in range(DIM):
        for c in range(DIM):
            available_board[r][c] = 0
            if is_vacant(board, r, c, piece):
                if orthello(board, r, c, piece, False):
                    playable_locs.append((r,c))
                    available_board[r][c] = piece
    # print(playable_locs)
    return playable_locs

# Function to check if location is vacant.
def is_vacant(board, row, col, piece):
    # print("Check vacant")
    return board[row][col] == 0

# Grand function!
'''
This function has 2 functions:
1. With the drop boolean set to false, it determines whether the placement of piece will lead to reversals.
2. With the drop boolean set to true, it actually drops the piece, and reverse the relevant pieces surounding it.
    This involves finding nearest piece (with opponent in between) in the vert/horz/diag axis and reversing the pieces.
Remember that the upper range (even if the range is in reverse direction - large to small) is non-inclusive.
    So for a bound from col x to 0, it should be [x, -1, -1]
'''
def orthello(board, row, col, piece, drop):
    flip_num = 0

    # Drop the piece
    if drop == True:
        print("Drop piece and reverse at row=", row, " col=", col)
        board[row][col] = piece
    else:
        pass
        # print("Can piece lead to reversal?")

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
            if board[row][c] == piece: # REVERSE!
                if c == (col+1): # Not reversible if piece on the immediate right is itself or empty
                    break
                if drop == False: # If drop == False, just the reversible status
                    return True
                # If drop == True, return boolean to indicate that pieces in between to be reversed.
                reverse = True
                opp_col = c
                break
        if reverse == True and drop == True:
            for c in range(col+1, opp_col):
                board[row][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse left (must check from right to left):
    if (col-1) >= 0:
        # print ("    check left", row, col)
        for c in range(col-1, -1, -1):
            if board[row][c] == 0:
                break
            if board[row][c] == piece:
                if c == (col-1):
                    break
                if drop == False:
                    return True
                reverse = True
                opp_col = c
                break
        if reverse == True and drop == True:
            for c in range(col-1, opp_col, -1):
                board[row][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row, ", col=",c)
        reverse = False

    # Reverse up (must check from down to up):
    if (row-1) >= 0:
        # print ("    check up", row, col)
        for r in range(row-1, -1, -1):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                if r == (row-1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = r
                break
        if reverse == True and drop == True:
            for r in range(row-1, opp_row, -1):
                board[r][col] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse down:
    if (row+1) <= DIM: # amended
        # print ("    check down", row, col)
        for r in range(row+1, DIM):
            if board[r][col] == 0:
                break
            if board[r][col] == piece:
                if r == (row+1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = r
                break
        if reverse == True and drop == True:
            for r in range(row+1, opp_row):
                board[r][col] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", r, ", col=",col)
        reverse = False

    # Reverse positive diagonal, left of chess (going up to the right, so rows decreasing):
    if (col-1) >= 0:
        # print ("    check positive diagonal left", row, col)
        row_it = row+1
        for c in range(col-1, -1, -1):
            if row_it >= DIM or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                if c == (col-1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it + 1
        if reverse == True and drop == True:
            row_it = row+1
            for c in range (col-1, opp_col, -1):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False

    # Reverse positive diagonal, right of chess:
    if (col+1) <= DIM:
        # print ("    check positive diagonal right", row, col)
        row_it = row-1
        for c in range(col+1, DIM):
            if row_it < 0 or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                if c == (col+1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it - 1
        if reverse == True and drop == True:
            row_it = row-1
            for c in range (col+1, opp_col):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it - 1
        reverse = False

    # Reverse negative diagonal, left of chess:
    if (col-1) >= 0:
        # print ("    check negative diagonal left", row, col)
        row_it = row-1
        for c in range(col-1, -1, -1):
            if (row_it) < 0 or board[row_it][c] == 0:
                break
            if board[row_it][c] == piece:
                if c == (col-1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it - 1
        if reverse == True and drop == True:
            row_it = row-1
            for c in range (col-1, opp_col, -1):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
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
                if c==(col+1):
                    break
                if drop == False: 
                    return True
                reverse = True
                opp_row = row_it
                opp_col = c
                break
            row_it = row_it + 1
        if reverse == True and drop == True:
            row_it = row+1
            for c in range (col+1, opp_col):
                board[row_it][c] = piece
                flip_num = flip_num+1
                print("         reverse piece at row=", row_it, ", col=",c)
                row_it = row_it + 1
        reverse = False
    
    if drop == False:
        return False
    else:
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
            pygame.draw.rect(screen, BLACK, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[r][c] == 1: # Player 1
                pygame.draw.circle(screen, WHITE, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                pygame.draw.circle(screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
            elif board[r][c] == 2: # Player 2
                pygame.draw.circle(screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            else:
                pass
    pygame.display.update()

def draw_avaiBoard(available_board, turn):
    # Draw background
    # print(available_board)
    screen.blit(wood_img, (0,0))
    for c in range(DIM):
        for r in range(DIM):
            pygame.draw.rect(screen, GREEN, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if available_board[r][c] == 1 and turn == 1: # Available moves for player 1
                pygame.draw.circle(screen, WHITE, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
            elif available_board[r][c] == 2 and turn == 2: # Available moves for player 2
                pygame.draw.circle(screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
            else:
                pass
    available_board = np.zeros((DIM,DIM))
    pygame.display.update()

# Blit player and statistics information
def print_statistics(board, turn):
    # print("blit player information")
    # print("turn", turn)
    pygame.draw.rect(screen, GRAY, (stats_box_top_left, stats_box_dim))
    pygame.draw.rect(screen, BLACK, (stats_box_top_left, stats_box_dim), 1)
    if turn == 2:
        player_label = myfont.render(("Player 2"), 1, BLACK)
    elif turn == 1:
        player_label = myfont.render(("Player 1"), 1, WHITE)
    screen.blit(player_label, player_centre)
    p1_score = np.count_nonzero(board==1)
    p2_score = np.count_nonzero(board==2)
    total_label = myfont.render((f"Total = {np.count_nonzero(board)}"), 1, WHITE)
    score1_label = myfont.render((f"P1 = {p1_score}"), 1, WHITE)
    score2_label = myfont.render((f"P2 = {p2_score}"), 1, BLACK)
    flip_label = myfont.render((f"Flipped = {flip_num}"), 1, WHITE)
    screen.blit(total_label, stats_line1_centre)
    screen.blit(score1_label, stats_line2_centre)
    screen.blit(score2_label, stats_line3_centre)
    screen.blit(flip_label, stats_line4_centre)
    pygame.display.update()

# Blit special error messages or win game messages on the top.
def print_special_message(board, available_board, turn, message):
    print(message)
    label = myfont.render(message, 1, WHITE)
    screen.blit(wood_img, (0,0))
    # draw_avaiBoard(available_board, turn)
    # draw_board(board)
    screen.blit(label, (20,500))
    pygame.display.update()
    pygame.time.wait(1500)

# Goes to next turn.
def next_turn(turn, next_turn, error):
    if error == False:
        if turn == 1:
            turn = 2
            next_turn = 1
        else:
            turn = 1
            next_turn = 2

#################################### INITIALISE VARIABLES ###########################################
board = create_board()
turn = random.randint(PLAYER, AI)
if turn == PLAYER:
    next_turn = AI
elif turn == AI:
    next_turn = PLAYER
available_board = create_avaiBoard(turn)
playable_list = availoc(board, available_board, 1)

player_valid = False
AI_valid = False

# pygame variables
pygame.init()
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("calibri",40)

##### First Blit #####

# Print boards
draw_avaiBoard(available_board, 1)
draw_board(board)
print_board(board, 0)

# Reiniialise variables?
game_over = False
on_move = False
error = False
playable_list = availoc(board, available_board, turn)

#################################### MAIN LOOP ###########################################
while not game_over:

    # Reinitialise glags and print statistics to debug window
    error = False
    print_statistics(board, turn)

    if len(playable_list) != 0:

        # PLAYER
        if turn == PLAYER:
            player_valid = False
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    on_move = False
                    print("turn = PLAYER")
                    pygame.draw.rect(screen, BLACK, (0,0,width, SQUARE_SIZE))

                    # Ask for Player input
                    pos_x = event.pos[0] # Zeroeth element is horizontal axis, first element is vertical axis
                    pos_y = event.pos[1]

                    if SQUARE_SIZE < pos_y < SQUARE_SIZE*(DIM+1)  and SQUARE_SIZE < pos_x < SQUARE_SIZE*(DIM+1) :          
                        u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                        u_col = int(math.floor(pos_x/SQUARE_SIZE))-1

                        # Check for valid location and drop piece
                        if is_vacant(board, u_row, u_col, PLAYER) and orthello(board, u_row, u_col, PLAYER, False):
                            player_valid = True
                            flip_num = orthello(board, u_row, u_col, PLAYER, True)
                            playable_list = availoc(board, available_board, next_turn)
                            draw_avaiBoard(available_board, next_turn)
                        else: # If the chosen location is on the board but not valid, PLAYER goes again.
                            error = True
                            print_special_message(board, available_board, turn,"Error. Position not valid. PLAYER go again.")
                            playable_list = availoc(board, available_board, PLAYER)
                            draw_avaiBoard(available_board, PLAYER)
                        
                        # Print and draw board.                     
                        print_board(board, flip_num)
                        draw_board(board)
                    
                    else: # If the chosen location is off the board, PLAYER goes again (what the hell)
                        print_special_message(board, available_board, turn, "Error. Position not valid. PLAYER go again.")
                        draw_avaiBoard(available_board, PLAYER)
                        draw_board(board)
            
        if turn == AI:
            pygame.time.wait(2000)
            AI_valid = False
            print("turn = AI")

            rand_row, rand_col = random.choice(playable_list)

            # Check for valid location and drop piece
            if is_vacant(board, rand_row, rand_col, AI) and orthello(board, rand_row, rand_col, AI, False):
                AI_valid = True
                flip_num = orthello(board, rand_row, rand_col, AI, True)
                playable_list = availoc(board, available_board, next_turn)
                draw_avaiBoard(available_board, next_turn)
            else: # If the chosen location is on the board but not valid, AI goes again.
                error = True
                print_special_message(board, available_board, turn,"Error. Position not valid. AI go again.")
                playable_list = availoc(board, available_board, AI)
                draw_avaiBoard(available_board, AI)
            
            # Print and draw board.                     
            print_board(board, flip_num)
            draw_board(board)

        # Check for end game
        if is_end_game(board):
            print("End Game. Who wins?")
            if (p2_score > p1_score):
                print_special_message(board, available_board, turn, "AI wins!")
            elif (p2_score == p1_score):
                print_special_message(board, available_board, turn, "It's a tie! You're both winners/ losers!")
            else:
                print_special_message(board, available_board, turn, "PLAYER wins!")
            game_over = True

        # Next move
        # If error = False             
        if turn == PLAYER and player_valid == True:
            turn = AI
            next_turn = PLAYER
        elif turn == AI and AI_valid == True:
            turn = PLAYER
            next_turn = AI
        else:
            pass

    else: # If either player cannot move, then move on to next player. Blit available locations for next player.
        on_move = False
        print_special_message(board, available_board, turn, (f"Can't Move! Player {turn} cannot move. It is player {next_turn}'s turn." % locals()))
        draw_avaiBoard(available_board, turn)
        draw_board(board)
        if turn == PLAYER:
            turn = AI
            next_turn = PLAYER
        else:
            turn = PLAYER
            next_turn = AI
        playable_list = availoc(board, available_board, turn)

