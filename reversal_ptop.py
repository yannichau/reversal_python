from reversal_helpers import *
import random

#################################### INITIALISE VARIABLES ####################################
first_move = random.randint(1, 2)

# Initialisations
game = Reversal()
game.initialise(first_move)

# First blit
playable_list = game.availoc(first_move)
game.draw_avaiBoard(first_move)
game.draw_board()
game.print_board(0)

# Reiniialise variables?
flip_num = 0
cant_move = 0
game_over = False
player_valid = False
error = False

#################################### MAIN LOOP ####################################

while not game_over:

    # Reinitialise glags and print statistics to debug window
    error = False
    game.print_statistics()

    if len(playable_list) != 0:
        cant_move = 0

        # Main game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                on_move = False

                print("turn =", game.turn)

                # Ask for Player input
                pos_x = event.pos[0] 
                pos_y = event.pos[1]

                # Check for valid position and drop piece
                if within_range(pos_x) and within_range(pos_y):          
                    u_row = int(math.floor(pos_y/SQUARE_SIZE))-1
                    u_col = int(math.floor(pos_x/SQUARE_SIZE))-1
                    if game.is_vacant(u_row, u_col, game.turn) and game.orthello(u_row, u_col, game.turn, False):
                        error = False
                        player_valid = True
                        flip_num = game.orthello(u_row, u_col, game.turn, True)
                    else: # If the chosen location is on the board but not valid, PLAYER goes again.
                        error = True
                else:
                    error = True                   
                if error == True: # If the chosen location is off the board, PLAYER goes again (what the hell)
                    game.print_special_message(f"Error. Position not valid. Player {game.turn} go again." % locals())

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
        elif player_valid:
            playable_list = game.availoc(game.next_turn)
            game.draw_avaiBoard(game.next_turn)
            game.print_board(flip_num)
            game.draw_board()

        # Draw board and move on to next step
        if player_valid:            
            game.next_player()
            player_valid = False

    else: # If either player cannot move, then move on to next player. Blit available locations for next player.
        cant_move += 1
        game.print_special_message((f"Can't Move! Player {game.turn} cannot move. It is player {game.next_turn}'s turn." % locals()))
        playable_list = game.availoc(game.next_turn)
        game.draw_avaiBoard(game.next_turn)
        game.draw_board()
        game.next_player()
        player_valid = False 
        if cant_move > 2:
            game.terminate_game()
            game_over = True     
            