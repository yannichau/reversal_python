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
PLAYER_1 = 1
PLAYER_2 = 2
EMPTY = 0

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (36, 173, 66)
BROWN = (198, 135, 17)
GRAY = (128, 128, 128)

# Screen Rendering Dimensions
SQUARE_SIZE = 70
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
message_centre = (SQUARE_SIZE, SQUARE_SIZE*int((DIM+2)/2))

################################## TEMPORARY VARIABLES #####################################
wood_img = pygame.image.load('light_wood.jpg')

##################################### CLASS ##########################################
"""
Master class for this game!
"""
class Reversal:

    # Function to Initiate
    def __init__(self):
        self.flip_num = 0
        self.board = np.zeros((DIM, DIM))
        self.available_board = np.zeros((DIM, DIM))

    # Should be run at the start of the game.
    def initialise(self, turn):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.myfont = pygame.font.SysFont("calibri", 30)
        self.turn = turn
        if self.turn == PLAYER:
            self.next_turn = AI
        else:
            self.next_turn = PLAYER
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        if turn == PLAYER:
            self.available_board[3][5] = 1
            self.available_board[5][3] = 1
            self.available_board[2][4] = 1
            self.available_board[4][2] = 1
        elif turn == AI:
            self.available_board[2][3] = 2
            self.available_board[3][2] = 2
            self.available_board[5][4] = 2
            self.available_board[4][5] = 2  

    # Function to check if location is vacant.
    def is_vacant(self, row, col, piece):
        return self.board[row][col] == 0 

    # Function to check if player can place piece.
    def can_play(self, piece):
        # print("Can play?")
        for r in range(DIM):
            for c in range(DIM):
                if self.is_vacant(r, c, piece):
                    if self.orthello(r, c, piece, False):
                        return True
        return False

    # Function to return a list of available locations.
    def availoc(self, piece):
        playable_locs = []
        # print("Return a list of playable locations.")
        for r in range(DIM):
            for c in range(DIM):
                self.available_board[r][c] = 0
                if self.is_vacant(r, c, piece):
                    if self.orthello(r, c, piece, False):
                        playable_locs.append((r,c))
                        self.available_board[r][c] = piece
        # print(playable_locs)
        return playable_locs

    # Grand function!
    '''
    This function has 2 functions:
    1. With the drop boolean set to false, it determines whether the placement of piece will lead to reversals.
    2. With the drop boolean set to true, it actually drops the piece, and reverse the relevant pieces surounding it.
        This involves finding nearest piece (with opponent in between) in the vert/horz/diag axis and reversing the pieces.
    Remember that the upper range (even if the range is in reverse direction - large to small) is non-inclusive.
        So for a bound from col x to 0, it should be [x, -1, -1]
    '''
    def orthello(self, row, col, piece, drop):
        flip_num = 0

        # Drop the piece
        if drop == True:
            print("Drop piece and reverse at row=", row, " col=", col)
            self.board[row][col] = piece
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
                if self.board[row][c] == 0:
                    break
                if self.board[row][c] == piece: # REVERSE!
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
                    self.board[row][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row, ", col=",c)
            reverse = False

        # Reverse left (must check from right to left):
        if (col-1) >= 0:
            # print ("    check left", row, col)
            for c in range(col-1, -1, -1):
                if self.board[row][c] == 0:
                    break
                if self.board[row][c] == piece:
                    if c == (col-1):
                        break
                    if drop == False:
                        return True
                    reverse = True
                    opp_col = c
                    break
            if reverse == True and drop == True:
                for c in range(col-1, opp_col, -1):
                    self.board[row][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row, ", col=",c)
            reverse = False

        # Reverse up (must check from down to up):
        if (row-1) >= 0:
            # print ("    check up", row, col)
            for r in range(row-1, -1, -1):
                if self.board[r][col] == 0:
                    break
                if self.board[r][col] == piece:
                    if r == (row-1):
                        break
                    if drop == False: 
                        return True
                    reverse = True
                    opp_row = r
                    break
            if reverse == True and drop == True:
                for r in range(row-1, opp_row, -1):
                    self.board[r][col] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", r, ", col=",col)
            reverse = False

        # Reverse down:
        if (row+1) <= DIM: # amended
            # print ("    check down", row, col)
            for r in range(row+1, DIM):
                if self.board[r][col] == 0:
                    break
                if self.board[r][col] == piece:
                    if r == (row+1):
                        break
                    if drop == False: 
                        return True
                    reverse = True
                    opp_row = r
                    break
            if reverse == True and drop == True:
                for r in range(row+1, opp_row):
                    self.board[r][col] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", r, ", col=",col)
            reverse = False

        # Reverse positive diagonal, left of chess (going up to the right, so rows decreasing):
        if (col-1) >= 0:
            # print ("    check positive diagonal left", row, col)
            row_it = row+1
            for c in range(col-1, -1, -1):
                if row_it >= DIM or self.board[row_it][c] == 0:
                    break
                if self.board[row_it][c] == piece:
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
                    self.board[row_it][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row_it, ", col=",c)
                    row_it = row_it + 1
            reverse = False

        # Reverse positive diagonal, right of chess:
        if (col+1) <= DIM:
            # print ("    check positive diagonal right", row, col)
            row_it = row-1
            for c in range(col+1, DIM):
                if row_it < 0 or self.board[row_it][c] == 0:
                    break
                if self.board[row_it][c] == piece:
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
                    self.board[row_it][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row_it, ", col=",c)
                    row_it = row_it - 1
            reverse = False

        # Reverse negative diagonal, left of chess:
        if (col-1) >= 0:
            # print ("    check negative diagonal left", row, col)
            row_it = row-1
            for c in range(col-1, -1, -1):
                if (row_it) < 0 or self.board[row_it][c] == 0:
                    break
                if self.board[row_it][c] == piece:
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
                    self.board[row_it][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row_it, ", col=",c)
                    row_it = row_it - 1
            reverse = False

        # Reverse negative diagonal, right of chess:
        if (col+1) <= DIM:
            # print ("    check negative diagonal right", row, col)
            row_it = row+1
            for c in range(col+1, DIM):
                if (row_it) >= DIM or self.board[row_it][c] == 0:
                    break
                if self.board[row_it][c] == piece:
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
                    self.board[row_it][c] = piece
                    flip_num = flip_num+1
                    print("         reverse piece at row=", row_it, ", col=",c)
                    row_it = row_it + 1
            reverse = False
        
        if drop == False:
            return False
        else:
            self.flip_num = flip_num
            return flip_num

    # Print board and scores
    def print_board(self, flip_num): 
        p1_score = np.count_nonzero(self.board == 1)
        p2_score = np.count_nonzero(self.board == 2)
        print("\nPlayer 1 pieces =", p1_score)
        print("Player 2 pieces =", p2_score)
        print("Number of flipped pieces: ", flip_num)
        print("Total number of pieces on the board: ", np.count_nonzero(self.board))
        print(self.board)

    # End game boolean (True if all entries are filled in)
    def is_end_game(self):
        for c in range(DIM):
            for r in range(DIM): 
                if self.board[r][c] == 0:
                    return False
        return True

    # End game
    def terminate_game(self):
        p1_score = np.count_nonzero(self.board == 1)
        p2_score = np.count_nonzero(self.board == 2)
        print("End Game. Who wins?")
        if (p2_score > p1_score):
            self.print_special_message("AI wins!")
        elif (p2_score == p1_score):
            self.print_special_message("It's a tie! You're both winners/ losers!")
        else:
            self.print_special_message("PLAYER wins!")

    # Draw Board (Graphics)
    def draw_board(self):
        # Draw background
        for c in range(DIM):
            for r in range(DIM):
                pygame.draw.rect(self.screen, BLACK, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                if self.board[r][c] == 1: # Player 1
                    pygame.draw.circle(self.screen, WHITE, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                    pygame.draw.circle(self.screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
                elif self.board[r][c] == 2: # Player 2
                    pygame.draw.circle(self.screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                else:
                    pass
        pygame.display.update()

    def draw_avaiBoard(self, turn):
        # Draw background
        # print(available_board)
        self.screen.blit(wood_img, (0, 0))
        for c in range(DIM):
            for r in range(DIM):
                pygame.draw.rect(self.screen, GREEN, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(self.screen, BLACK, ((c+1)*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
                if self.available_board[r][c] == 1 and turn == 1: # Available moves for player 1
                    pygame.draw.circle(self.screen, WHITE, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
                elif self.available_board[r][c] == 2 and turn == 2: # Available moves for player 2
                    pygame.draw.circle(self.screen, BLACK, (int((c+1)*SQUARE_SIZE+SQUARE_SIZE/2), int((r+1)*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS, 2)
                else:
                    pass
        self.available_board = np.zeros((DIM, DIM))
        pygame.display.update()

    # Blit player and statistics information
    def print_statistics(self):
        pygame.draw.rect(self.screen, GRAY, (stats_box_top_left, stats_box_dim))
        pygame.draw.rect(self.screen, BLACK, (stats_box_top_left, stats_box_dim), 1)
        if self.turn == 2:
            player_label = self.myfont.render(("Player 2"), 1, BLACK)
        elif self.turn == 1:
            player_label = self.myfont.render(("Player 1"), 1, WHITE)
        self.screen.blit(player_label, player_centre)
        p1_score = np.count_nonzero(self.board == 1)
        p2_score = np.count_nonzero(self.board == 2)
        total_label = self.myfont.render((f"Total = {np.count_nonzero(self.board)}"), 1, WHITE)
        score1_label = self.myfont.render((f"Player 1 = {p1_score}"), 1, WHITE)
        score2_label = self.myfont.render((f"Player 2 = {p2_score}"), 1, BLACK)
        flip_label = self.myfont.render((f"Flipped = {self.flip_num}"), 1, WHITE)
        self.screen.blit(total_label, stats_line1_centre)
        self.screen.blit(score1_label, stats_line2_centre)
        self.screen.blit(score2_label, stats_line3_centre)
        self.screen.blit(flip_label, stats_line4_centre)
        pygame.display.update()

    # Blit special error messages or win game messages on the top.
    def print_special_message(self, message):
        print(message)
        label = self.myfont.render(message, 1, WHITE)
        self.screen.blit(wood_img, (0, 0))
        self.screen.blit(label, message_centre)
        pygame.display.update()
        self.print_statistics()
        pygame.time.wait(2500)

    # Goes to next turn.
    def next_player(self):
        if self.turn == 1:
            self.turn = 2
            self.next_turn = 1
        else:
            self.turn = 1
            self.next_turn = 2

class Reversal_AI(Reversal):
    
    # Designate scores for positions available on the board (which is the temporary board where the test piece is inserted)
    def score_position(self, turn):
        score = 0

        opp_turn = PLAYER
        if turn == PLAYER:
                opp_turn = AI
        
        # Own Advantage points - borders
        left_array = [int(i) for i in list(self.board[:,0])]
        right_array = [int(i) for i in list(self.board[:,DIM-1])]
        top_array = [self.board[0][i] for i in range(1, DIM-1)] # excluding first and last locations
        bott_array = [self.board[DIM-1][i] for i in range(1, DIM-1)] # excluding first and last locations
        border_count = left_array.count(turn) + right_array.count(turn) + top_array.count(turn) + bott_array.count(turn)
        # border_count_opp = left_array.count(opp_turn) + right_array.count(opp_turn) + top_array.count(opp_turn) + bott_array.count(opp_turn)
        score = score + border_count*10 # - border_count_opp*35

        # Own Advantage points - corners
        corners = [self.board[0][0], self.board[0][DIM-1], self.board[DIM-1][0], self.board[DIM-1][DIM-1]]
        corner_count = corners.count(turn)
        # corner_count_opp = corners.count(opp_turn)
        score = score + corner_count*100 # - corner_count_opp*100

        # Number of flipped pieces for the given move (just for a small offset)
        # score += flip_num

        # Advantage points of opponent in next move
        next_board = Reversal()
        next_board.board = self.board.copy()
        next_availist = next_board.availoc(opp_turn)
        next_corners = [(0, 0), (0, DIM-1), (DIM-1, 0), (DIM-1, DIM-1)]
        next_corner_count = next_availist.count(next_corners)
        next_left_array = [int(i) for i in list(next_board.available_board[:, 0])]
        next_right_array = [int(i) for i in list(next_board.available_board[:, DIM-1])]
        next_top_array = [next_board.available_board[0][i] for i in range(1, DIM-1)]
        next_bott_array = [next_board.available_board[DIM-1][i] for i in range(1, DIM-1)]
        next_border_count = next_left_array.count(opp_turn) + next_right_array.count(opp_turn) + next_top_array.count(opp_turn) + next_bott_array.count(opp_turn)
        score = score - next_corner_count*500 - next_border_count*50

        # Consider if own position is immediately flipped afterwards?

        return score

    # Picks the best move based on the current board only.
    def pick_best_move(self, turn):
        best_score = -10000
        valid_locations = self.availoc(turn)
        best_row, best_col = random.choice(valid_locations) # initialise with random location.
        for loc in valid_locations:
            best_row, best_col = loc
            temp = Reversal_AI()
            temp.board = self.board.copy()
            temp.available_board = self.available_board.copy()
            flip_num = temp.orthello(best_row, best_col, turn, True) 
            score = temp.score_position(turn)
            if score > best_score:
                best_score = score
                best_loc = best_row, best_col
        return best_loc

    # Blit player and statistics information (override)
    def print_statistics(self):
        pygame.draw.rect(self.screen, GRAY, (stats_box_top_left, stats_box_dim))
        pygame.draw.rect(self.screen, BLACK, (stats_box_top_left, stats_box_dim), 1)
        if self.turn == 2:
            player_label = self.myfont.render(("AI"), 1, BLACK)
        elif self.turn == 1:
            player_label = self.myfont.render(("PLAYER"), 1, WHITE)
        self.screen.blit(player_label, player_centre)
        p1_score = np.count_nonzero(self.board == 1)
        p2_score = np.count_nonzero(self.board == 2)
        total_label = self.myfont.render((f"Total = {np.count_nonzero(self.board)}"), 1, WHITE)
        score1_label = self.myfont.render((f"PLAYER = {p1_score}"), 1, WHITE)
        score2_label = self.myfont.render((f"AI = {p2_score}"), 1, BLACK)
        flip_label = self.myfont.render((f"Flipped = {self.flip_num}"), 1, WHITE)
        self.screen.blit(total_label, stats_line1_centre)
        self.screen.blit(score1_label, stats_line2_centre)
        self.screen.blit(score2_label, stats_line3_centre)
        self.screen.blit(flip_label, stats_line4_centre)
        pygame.display.update()

    # Blit special error messages or win game messages on the top. (override)
    def print_special_message(self, message):
        print(message)
        message = message.replace("Player 1", "PLAYER")
        message = message.replace("Player 2", "AI")
        message = message.replace("player 2", "AI")
        label = self.myfont.render(message, 1, WHITE)
        self.screen.blit(wood_img, (0, 0))
        self.screen.blit(label, message_centre)
        pygame.display.update()
        self.print_statistics()
        pygame.time.wait(2500)

# Minimax Algorithm for finding the the best move
def minimax(board, depth, alpha, beta, maximizingPlayer, turn):

    temp = Reversal_AI()
    temp.board = board.copy()
    valid_locations = temp.availoc(turn)

    if depth == 0 or len(valid_locations)== 0: # not useful to know the terminal node of the game
        return (None, None, temp.score_position(AI))

    if maximizingPlayer:
        value = -math.inf
        best_row, best_col = random.choice(valid_locations)
        for loc in valid_locations:
            row, col = loc
            temp_new = Reversal()
            temp_new.board = temp.board.copy()
            dummy = temp_new.orthello(row, col, AI, True)
            new_score = minimax(temp_new.board, depth-1, alpha, beta, False, AI)[2]
            if new_score > value:
                value = new_score
                best_row = row
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_row, best_col, value

    else: # Minimizing player
        value = math.inf
        best_row, best_col = random.choice(valid_locations)
        for loc in valid_locations:
            row, col = loc
            temp_new = Reversal()
            temp_new.board = temp.board.copy()
            dummy = temp_new.orthello(row, col, PLAYER, True)
            new_score = minimax(temp_new.board, depth-1, alpha, beta, True, PLAYER)[2]
            if new_score < value:
                value = new_score
                best_row = row
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_row, best_col, value

def within_range(pos):
    if SQUARE_SIZE < pos < SQUARE_SIZE*(DIM+1):
        return True
    return False