from reversal_helpers import *
import random

#################################### INITIALISE VARIABLES ###########################################
turn = random.randint(PLAYER, AI)
if turn == PLAYER:
    next_turn = AI
elif turn == AI:
    next_turn = PLAYER

game = Reversal()
game.initialise(turn)
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
        if game.turn == PLAYER:
            player_valid = False
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("turn = PLAYER")
                    # pygame.draw.rect(game.screen, BLACK, (0,0,width, SQUARE_SIZE))

                    # Ask for Player input
                    pos_x = event.pos[0] # Zeroeth element is horizontal axis, first element is vertical axis
                    pos_y = event.pos[1]

                    if SQUARE_SIZE < pos_y < SQUARE_SIZE*(DIM+1)  and SQUARE_SIZE < pos_x < SQUARE_SIZE*(DIM+1):          
                        u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                        u_col = int(math.floor(pos_x/SQUARE_SIZE))-1
                        # Check for valid location and drop piece
                        if game.is_vacant(u_row, u_col, PLAYER) and game.orthello(u_row, u_col, PLAYER, False):
                            player_valid = True
                            flip_num = game.orthello(u_row, u_col, PLAYER, True)
                            playable_list = game.availoc(AI)
                            game.draw_avaiBoard(AI)
                        else: # If the chosen location is on the board but not valid, PLAYER goes again.
                            error = True
                    else:
                        error = True
                    
                    if error == True: # If the chosen location is off the board, PLAYER goes again (what the hell)
                        game.print_special_message("Error. Position not valid. PLAYER go again.")
                        playable_list = game.availoc(PLAYER)
                        game.draw_avaiBoard(PLAYER)

                    # Print and draw board
                    game.print_board(flip_num)
                    game.draw_board()
            
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
                playable_list = game.availoc(PLAYER)
                game.draw_avaiBoard(PLAYER)
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
        if (game.turn == PLAYER and player_valid == True) or (game.turn == AI and AI_valid == True):
            game.next_player() 


    else: # If either player cannot move, then move on to next player. Blit available locations for next player.
        cant_move += 1
        game.print_special_message((f"Can't Move! Player {turn} cannot move. It is player {next_turn}'s turn." % locals()))
        game.next_player()
        playable_list = game.availoc(game.turn)
        game.draw_avaiBoard(game.turn)
        game.draw_board()
        if cant_move > 2:
            game.terminate_game()
            game_over = True

