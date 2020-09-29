from reversal_helpers import *
import random

#################################### INITIALISE VARIABLES ###########################################
first_move = random.randint(PLAYER, AI)

# Initialisations
game = Reversal_AI()
game.initialise(first_move)

# First blit
playable_list = game.availoc(first_move)
game.draw_avaiBoard(first_move)
game.draw_board()
game.print_board(0)

# Reiniialise variables?
flip_num = 0
cant_move = 0
player_valid, AI_valid = False, False
game_over = False
error = False

#################################### MAIN LOOP ###########################################
while not game_over:

    # Reinitialise glags and print statistics to debug window
    error = False
    game.print_statistics()

    if len(playable_list) != 0:
        cant_move = 0

        # PLAYER
        if game.turn == PLAYER:
            player_valid = False
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("turn = PLAYER")

                    # Ask for Player input
                    pos_x = event.pos[0] 
                    pos_y = event.pos[1]
                    
                    # If within valid position
                    if within_range(pos_x) and within_range(pos_y):          
                        u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                        u_col = int(math.floor(pos_x/SQUARE_SIZE))-1
                        # Check for valid location and drop piece
                        if game.is_vacant(u_row, u_col, PLAYER) and game.orthello(u_row, u_col, PLAYER, False):
                            player_valid = True
                            flip_num = game.orthello(u_row, u_col, PLAYER, True)
                        else: # If the chosen location is on the board but not valid, PLAYER goes again.
                            error = True
                    else:
                        error = True                   
                    if error == True: # If the chosen location is off the board, PLAYER goes again (what the hell)
                        game.print_special_message("Error. Position not valid. PLAYER go again.")

        # AI  
        if game.turn == AI:
            AI_valid = False
            print("turn = AI")
            # row, col = random.choice(playable_list)
            # row, col = pick_best_move(board, available_board, turn)
            row, col, minimax_score = minimax(game.board, 4, -math.inf, math.inf, True, AI)

            # Check for valid location and drop piece
            if game.is_vacant(row, col, AI) and game.orthello(row, col, AI, False):
                AI_valid = True
                flip_num = game.orthello(row, col, AI, True)
            else: # If the chosen location is on the board but not valid, AI goes again.
                error = True
                game.print_special_message("Error. Position not valid. AI go again.")
            
        # Check for end game
        if game.is_end_game():
            game.terminate_game()
            game_over = True

        # Draw available move
        if error == True:
            playable_list = game.availoc(game.turn)
            game.draw_avaiBoard(game.turn)
            game.print_board(flip_num)
            game.draw_board()
        elif player_valid or AI_valid:
            playable_list = game.availoc(game.next_turn)
            game.draw_avaiBoard(game.next_turn)
            game.print_board(flip_num)
            game.draw_board()

        # Draw board and move on to next step
        
        if (game.turn == PLAYER and player_valid == True) or (game.turn == AI and AI_valid == True):            
            game.next_player()
            player_valid, AI_valid = False, False

    else: # If either player cannot move, then move on to next player. Blit available locations for next player.
        cant_move += 1
        game.print_special_message((f"Can't Move! Player {game.turn} cannot move. It is player {game.next_turn}'s turn." % locals()))
        playable_list = game.availoc(game.next_turn)
        game.draw_avaiBoard(game.next_turn)
        game.draw_board()
        game.next_player()
        player_valid, AI_valid = False, False
        if cant_move > 2:
            game.terminate_game()
            game_over = True

