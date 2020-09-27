from reversal_helpers import *
import random

# Minimax Algorithm for finding the the best move
def minimax(board, depth, alpha, beta, maximizingPlayer, turn):

    temp = Reversal(turn)
    temp.board = board.copy()
    valid_locations = temp.availoc(turn)

    if depth == 0 or len(valid_locations)== 0: # not useful to know the terminal node of the game
        return (None, None, temp.score_position(AI))

    if maximizingPlayer:
        value = -math.inf
        best_row, best_col = random.choice(valid_locations)
        for loc in valid_locations:
            row, col = loc
            temp_new = Reversal(turn)
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
            temp_new = Reversal(turn)
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

#################################### INITIALISE VARIABLES ###########################################
turn = random.randint(PLAYER, AI)
if turn == PLAYER:
    next_turn = AI
elif turn == AI:
    next_turn = PLAYER

game = Reversal(turn)
playable_list = game.availoc(turn)

# First blit
game.draw_avaiBoard(turn)
game.draw_board()
game.print_board(0)

# Reiniialise variables?
flip_num = 0
playable_list = []
player_valid = False
AI_valid = False
cant_move = 0
game_over = False
error = False
playable_list = game.availoc(turn)

#################################### MAIN LOOP ###########################################
while not game_over:

    # Reinitialise glags and print statistics to debug window
    error = False
    game.print_statistics()

    if len(playable_list) != 0:
        cant_move = 0

        # PLAYER
        if turn == PLAYER:
            player_valid = False
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("turn = PLAYER")
                    pygame.draw.rect(game.screen, BLACK, (0,0,width, SQUARE_SIZE))

                    # Ask for Player input
                    pos_x = event.pos[0] # Zeroeth element is horizontal axis, first element is vertical axis
                    pos_y = event.pos[1]

                    if SQUARE_SIZE < pos_y < SQUARE_SIZE*(DIM+1)  and SQUARE_SIZE < pos_x < SQUARE_SIZE*(DIM+1) :          
                        u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                        u_col = int(math.floor(pos_x/SQUARE_SIZE))-1

                        # Check for valid location and drop piece
                        if game.is_vacant(u_row, u_col, PLAYER) and game.orthello(u_row, u_col, PLAYER, False):
                            player_valid = True
                            flip_num = game.orthello(u_row, u_col, PLAYER, True)
                            playable_list = game.availoc(next_turn)
                            game.draw_avaiBoard(next_turn)
                        else: # If the chosen location is on the board but not valid, PLAYER goes again.
                            error = True
                            game.print_special_message("Error. Position not valid. PLAYER go again.")
                            playable_list = game.availoc(PLAYER)
                            game.draw_avaiBoard(PLAYER)
                        
                        # Print and draw board.                     
                        game.print_board(flip_num)
                        game.draw_board()
                    
                    else: # If the chosen location is off the board, PLAYER goes again (what the hell)
                        game.print_special_message("Error. Position not valid. PLAYER go again.")
                        game.draw_avaiBoard(PLAYER)
                        game.draw_board()
            
        if turn == AI:
            # pygame.time.wait(3000)
            AI_valid = False
            print("turn = AI")

            # row, col = random.choice(playable_list)
            # row, col = pick_best_move(board, available_board, turn)
            row, col, minimax_score = minimax(game.board, 4, -math.inf, math.inf, True, AI)

            # Check for valid location and drop piece
            if game.is_vacant(row, col, AI) and game.orthello(row, col, AI, False):
                AI_valid = True
                flip_num = game.orthello(row, col, AI, True)
                playable_list = game.availoc(next_turn)
                game.draw_avaiBoard(next_turn)
            else: # If the chosen location is on the board but not valid, AI goes again.
                error = True
                game.print_special_message("Error. Position not valid. AI go again.")
                playable_list = game.availoc(AI)
                game.draw_avaiBoard(AI)
            
            # Print and draw board.                     
            game.print_board(flip_num)
            game.draw_board()

        # Check for end game
        if game.is_end_game():
            game.terminate_game()
            game_over = True

        # Next move
        # If error = False       
        if turn == PLAYER and player_valid == True:
            game.next_player(False) 
            turn = AI
            next_turn = PLAYER
        elif turn == AI and AI_valid == True:
            game.next_player(False) 
            turn = PLAYER
            next_turn = AI
        else:
            pass

    else: # If either player cannot move, then move on to next player. Blit available locations for next player.
        cant_move += 1
        game.print_special_message((f"Can't Move! Player {turn} cannot move. It is player {next_turn}'s turn." % locals()))
        game.next_player(False)
        if turn == PLAYER:
            turn = AI
            next_turn = PLAYER
        else:
            turn = PLAYER
            next_turn = AI
        playable_list = game.availoc(turn)
        game.draw_avaiBoard(turn)
        game.draw_board()
        if cant_move > 2:
            game.terminate_game()
            game_over = True

