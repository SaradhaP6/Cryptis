import pygame
import os
from keys import generate_private_key, generate_public_key
from messages import generate_message, message_to_ternary, ternary_to_message, encode_message
from block import BlockTab
import time


"""
Variables
"""
### Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_PURPLE_COLOR = (224, 170, 255)
DARK_PURPLE_COLOR = (123, 44, 191)
BLOCK_SIZE_DEFAULT = (50, 10)

### Multiple use variables
# Buttons color
button_color = LIGHT_PURPLE_COLOR
button_hover_color = DARK_PURPLE_COLOR
# Paths
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
# Logo
logo_path = os.path.join(current_dir, "../img/logo.png")
logo_path = os.path.abspath(logo_path)
try:
    logo = pygame.image.load(logo_path)
    logo_img = pygame.transform.scale_by(logo, 0.6)
    logo_playing = pygame.transform.scale_by(logo, 0.3)
except:
    print("Error when loading the logo image")
    logo_img = pygame.Surface((100, 50))
    logo_img.fill(BLACK_COLOR)
    logo_playing = pygame.Surface((50, 25))
    logo_playing.fill(BLACK_COLOR)

### pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cryptris by Saradha")
clock = pygame.time.Clock()
running = True

### Elements for menu
game_state = "menu"
# Start button
start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100//2, 450, 100, 50)
# Game mode selection button
game_mode_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100//2, 525, 100, 50)
# Text on menu page
font = pygame.font.Font(None, 30)
title_text1 = font.render("by Saradha", True, WHITE_COLOR)
title_text2 = font.render("Based on the game, Cryptris,", True, WHITE_COLOR)
title_text3 = font.render("developped by Digital Cuisine & Inria", True, WHITE_COLOR)

### Elements for the mode selection page
# Solo button
solo_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100//2, 400, 100, 50)
# Player vs Bot button
vsBot_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150//2, 475, 150, 50)

### Elements for the winning page
# Congrats image
congrats_path = os.path.join(current_dir, "../img/congrats.png")
congrats_path = os.path.abspath(congrats_path)
try:
    congrats_img = pygame.image.load(congrats_path)
except:
    print("Error when loading the congrats image")
    congrats_img = pygame.Surface((100, 50))
    congrats_img.fill(BLACK_COLOR)

### Elements for the loosing page
# Game Over image
gameover_path = os.path.join(current_dir, "../img/game_over.png")
gameover_path = os.path.abspath(gameover_path)
try:
    gameover_img = pygame.image.load(gameover_path)
except:
    print("Error when loading the game over image")
    gameover_img = pygame.Surface((100, 50))
    gameover_img.fill(BLACK_COLOR)

### Elements for the game
# Keys and messages
private_key = []
public_key = []
encoded_message = []
decoded_message = []
rotation_index = 0
sign_inversion = 1
key_falling = False
private_key_tab = None
encoded_message_tab = None
# Key use help image
key_use_path = os.path.join(current_dir, "../img/key_use.png")
key_use_path = os.path.abspath(key_use_path)
try:
    key_use_img = pygame.image.load(key_use_path)
    key_use_img = pygame.transform.scale_by(key_use_img, 0.6)
except:
    print("Error when loading the game over image")
    key_use_img = pygame.Surface((100, 50))
    key_use_img.fill(BLACK_COLOR)
# Timer setup
start_time = None
time_limit = 120
# Game mode
game_mode = "solo"
# Playing vs Bot
botPlayingWithPrivateKey = False
bot_last_move_time = None
bot_using_key = []
bot_encoded_message = []
bot_decoded_message = []
bot_using_key_tab = None
bot_encoded_message_tab = None
bot_waiting_time = 1



"""
Functions
"""
def initialize_game():

    global private_key, public_key, message, ternary_message, start_time
    global private_key_tab, encoded_message, decoded_message, encoded_message_tab
    global bot_using_key, bot_encoded_message, bot_using_key_tab, bot_encoded_message_tab
    global bot_last_move_time, bot_decoded_message, bot_waiting_time

    private_key = generate_private_key(8)
    public_key = generate_public_key(private_key)
    message = generate_message(8)
    ternary_message = message_to_ternary(message)
    encoded_message = encode_message(ternary_message, public_key)
    decoded_message = ternary_to_message(encoded_message)

    if game_mode == "solo":

        private_key_tab = BlockTab(
            x_first_column=395,
            y_first_line=50,
            number_blocks_per_column=private_key,
            column_direction=-1,
            block_size=BLOCK_SIZE_DEFAULT
        )
        encoded_message_tab = BlockTab(
            x_first_column=395,
            y_first_line=675,
            number_blocks_per_column=encoded_message,
            column_direction=1,
            block_size=BLOCK_SIZE_DEFAULT
        )

    elif game_mode == "vsBot":

        private_key_tab = BlockTab(
            x_first_column=75,
            y_first_line=50,
            number_blocks_per_column=private_key,
            column_direction=-1,
            block_size=BLOCK_SIZE_DEFAULT
        )
        encoded_message_tab = BlockTab(
            x_first_column=75,
            y_first_line=675,
            number_blocks_per_column=encoded_message,
            column_direction=1,
            block_size=BLOCK_SIZE_DEFAULT
        )

        for letter in encoded_message:
            bot_encoded_message.append(letter)

        bot_decoded_message = ternary_to_message(bot_encoded_message)
        
        if not botPlayingWithPrivateKey:
            for m in public_key:
                bot_using_key.append(m)
        else:
            for n in private_key:
                bot_using_key.append(n)

        bot_using_key_tab = BlockTab(
            x_first_column=800,
            y_first_line=50,
            number_blocks_per_column=bot_using_key,
            column_direction=-1,
            block_size=BLOCK_SIZE_DEFAULT
        )
        bot_encoded_message_tab = BlockTab(
            x_first_column=800,
            y_first_line=675,
            number_blocks_per_column=bot_encoded_message,
            column_direction=1,
            block_size=BLOCK_SIZE_DEFAULT
        )

        if botPlayingWithPrivateKey:
            bot_waiting_time = 3
    
    start_time = time.time()
    bot_last_move_time = time.time()

    print("New game initialized")

def bot_next_move():
    global bot_using_key, bot_encoded_message, bot_decoded_message

    if not botPlayingWithPrivateKey:
        best_choice = 0
        inversed = False
        maximum_reduced_blocks = 0
        key_length = len(bot_using_key)

        for rotation in range(key_length):
            rotated_bot_using_key = bot_using_key[rotation:] + bot_using_key[:rotation]

            temp_add_bot_encoded_message = [val1 for val1 in bot_encoded_message]
            temp_substract_bot_encoded_message = [val2 for val2 in bot_encoded_message]
            for a in range(key_length):
                temp_add_bot_encoded_message[a] += rotated_bot_using_key[a]
                temp_substract_bot_encoded_message[a] -= rotated_bot_using_key[a]

            reduced_blocks_add = 0
            reduced_blocks_substract = 0
            for b in range(key_length):
                reduced_blocks_add += abs(bot_encoded_message[b]) - abs(temp_add_bot_encoded_message[b])
                reduced_blocks_substract += abs(bot_encoded_message[b]) - abs(temp_substract_bot_encoded_message[b])
            
            if reduced_blocks_add > reduced_blocks_substract and reduced_blocks_add > maximum_reduced_blocks:
                maximum_reduced_blocks = reduced_blocks_add
                best_choice = rotation
                inversed = False
            elif reduced_blocks_substract > reduced_blocks_add and reduced_blocks_substract > maximum_reduced_blocks:
                maximum_reduced_blocks = reduced_blocks_substract
                best_choice = rotation
                inversed = True

        bot_using_key = bot_using_key[best_choice:] + bot_using_key[:best_choice]

        if inversed:
            bot_using_key = [-value for value in bot_using_key]

        for d in range(key_length):
            bot_encoded_message[d] += bot_using_key[d]
        
        bot_decoded_message = ternary_to_message(bot_encoded_message)



"""
Main loop
"""
while running:

    clock.tick(FPS)

    # Timer (only if mode = solo)
    if game_mode == "solo":
        if game_state == "playing" and start_time:
            game_elapsed_time = time.time() - start_time
            if game_elapsed_time >= time_limit:
                game_state = "lost"

    # Events from player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN :
            if start_button_rect.collidepoint(event.pos):
                initialize_game()
                print("Private Key:", private_key)
                print("Initial Message:", message)
                print("Initial Ternary Message:", ternary_message)
                print("Encoded Message:", encoded_message)
                game_state = "playing"
            elif game_mode_button_rect.collidepoint(event.pos):
                game_state = "ModeSelection"
        elif game_state == "ModeSelection" and event.type == pygame.MOUSEBUTTONDOWN :
            if solo_button_rect.collidepoint(event.pos):
                game_mode = "solo"
                game_state = "menu"
            elif vsBot_button_rect.collidepoint(event.pos):
                game_mode = "vsBot"
                game_state = "menu"
        elif game_state == "playing" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                private_key = private_key[1:] + private_key[:1]
            elif event.key == pygame.K_RIGHT:
                private_key = private_key[-1:] + private_key[:-1]
            elif event.key == pygame.K_UP:
                sign_inversion *= -1
                private_key = [-val for val in private_key]
            elif event.key == pygame.K_RETURN:
                key_falling = True
        
    screen.fill(BLACK_COLOR)

    # Main menu
    if game_state == "menu":

        mouse_pos = pygame.mouse.get_pos()

        # If the player is hovering on the Start button
        if start_button_rect.collidepoint(mouse_pos):
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 370))
            screen.blit(title_text3, (SCREEN_WIDTH // 2 - title_text3.get_width() // 2, 400))

            # Start button
            pygame.draw.rect(screen, button_hover_color, start_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=start_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Game mode button
            pygame.draw.rect(screen, button_color, game_mode_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Mode", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=game_mode_button_rect.center)
            screen.blit(text_surface, text_rect)

        # If the player is hovering on the Game mode button
        elif game_mode_button_rect.collidepoint(mouse_pos):
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 370))
            screen.blit(title_text3, (SCREEN_WIDTH // 2 - title_text3.get_width() // 2, 400))

            # Start button
            pygame.draw.rect(screen, button_color, start_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=start_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Game mode button
            pygame.draw.rect(screen, button_hover_color, game_mode_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Mode", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=game_mode_button_rect.center)
            screen.blit(text_surface, text_rect)

        # If the player's mouse is not on the buttons
        else:
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 370))
            screen.blit(title_text3, (SCREEN_WIDTH // 2 - title_text3.get_width() // 2, 400))

            # Start button
            pygame.draw.rect(screen, button_color, start_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=start_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Game mode button
            pygame.draw.rect(screen, button_color, game_mode_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Mode", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=game_mode_button_rect.center)
            screen.blit(text_surface, text_rect)
    
    # Mode selection page
    elif game_state == "ModeSelection":
        
        mouse_pos = pygame.mouse.get_pos()

        # If the player is hovering on the Solo mode button
        if solo_button_rect.collidepoint(mouse_pos):
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))

            # Solo mode button
            pygame.draw.rect(screen, button_hover_color, solo_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Solo", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=solo_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Player vs Bot mode button
            pygame.draw.rect(screen, button_color, vsBot_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Player vs Bot", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=vsBot_button_rect.center)
            screen.blit(text_surface, text_rect)

        # If the player is hovering on the Player vs Bot mode button
        elif vsBot_button_rect.collidepoint(mouse_pos):
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))

            # Solo mode button
            pygame.draw.rect(screen, button_color, solo_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Solo", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=solo_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Player vs Bot mode button
            pygame.draw.rect(screen, button_hover_color, vsBot_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Player vs Bot", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=vsBot_button_rect.center)
            screen.blit(text_surface, text_rect)

        # If the player's mouse is not on the buttons
        else :
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))

            # Solo mode button
            pygame.draw.rect(screen, button_color, solo_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Solo", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=solo_button_rect.center)
            screen.blit(text_surface, text_rect)

            # Player vs Bot mode button
            pygame.draw.rect(screen, button_color, vsBot_button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Player vs Bot", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=vsBot_button_rect.center)
            screen.blit(text_surface, text_rect)

    # Playing screen
    elif game_state == "playing":

        # Updating the blocks' size if too much blocks
        max_private_key = max(abs(val) for val in private_key)
        max_encoded_message = max(abs(val) for val in encoded_message)
        total_max = max_private_key + max_encoded_message
        if total_max > 50:
            blocks_size = (50, 5)
        else:
            blocks_size = BLOCK_SIZE_DEFAULT

        # Background for the playing screen
        screen.fill(BLACK_COLOR)

        # Display of the timer
        if game_mode == "solo":
            remaining_time = max(0, time_limit - (time.time() - start_time))
            font = pygame.font.Font(None, 30)
            timer_text = font.render(f"Time left: {int(remaining_time)} seconds", True, LIGHT_PURPLE_COLOR)
            screen.blit(timer_text, (10, 10))
        elif game_mode == "vsBot":
            time_played = max(0, time.time() - start_time)
            font = pygame.font.Font(None, 30)
            timer_text = font.render(f"Time played: {int(time_played)} seconds", True, LIGHT_PURPLE_COLOR)
            screen.blit(timer_text, (10, 10))

        # Update of key(s) blocks
        if game_mode == "solo":
            private_key_tab = BlockTab(
                x_first_column=395,
                y_first_line=50,
                number_blocks_per_column=private_key,
                column_direction=-1,
                block_size=blocks_size
            )
        elif game_mode == "vsBot":
            private_key_tab = BlockTab(
                x_first_column=75,
                y_first_line=50,
                number_blocks_per_column=private_key,
                column_direction=-1,
                block_size=blocks_size
            )
            bot_using_key_tab = BlockTab(
                x_first_column=800,
                y_first_line=50,
                number_blocks_per_column=bot_using_key,
                column_direction=-1,
                block_size=BLOCK_SIZE_DEFAULT
            )

        # Displaying the decoded message
        font = pygame.font.Font(None, 30)
        decoded_text = font.render(f"Message: {decoded_message}", True, LIGHT_PURPLE_COLOR)
        if game_mode == "solo":
            screen.blit(decoded_text, (515, SCREEN_HEIGHT - 30))
        elif game_mode == "vsBot":
            screen.blit(decoded_text, (200, SCREEN_HEIGHT - 30))
            bot_decoded_text = font.render(f"Message: {bot_decoded_message}", True, LIGHT_PURPLE_COLOR)
            screen.blit(bot_decoded_text, (920, SCREEN_HEIGHT - 30))

        # Displaying the key to use to play
        if game_mode == "solo":
            screen.blit(key_use_img, (850, SCREEN_HEIGHT//2 - key_use_img.get_height()//2))
        elif game_mode == "vsBot":
            screen.blit(key_use_img, (SCREEN_WIDTH//2 - key_use_img.get_width()//2, SCREEN_HEIGHT//2 - key_use_img.get_height()//2))

        # Drawing private key
        private_key_tab.draw(screen)

        # Falling key: Updating encoded message value
        if key_falling:
            for i in range(len(private_key)):
                encoded_message[i] += private_key[i]
            # Updating of the encoded message's blocks
            if game_mode == "solo":
                encoded_message_tab = BlockTab(
                    x_first_column=395,
                    y_first_line=675,
                    number_blocks_per_column=encoded_message,
                    column_direction=1,
                    block_size=blocks_size
                )
            elif game_mode == "vsBot":
                encoded_message_tab = BlockTab(
                    x_first_column=75,
                    y_first_line=675,
                    number_blocks_per_column=encoded_message,
                    column_direction=1,
                    block_size=blocks_size
                )
            decoded_message = ternary_to_message(encoded_message)
            key_falling = False
        
        #Drawing encoded message
        encoded_message_tab.draw(screen)

        # Updating bot using key & encoded message
        if time.time() - bot_last_move_time > bot_waiting_time:
            bot_next_move()
            bot_last_move_time = time.time()

        bot_encoded_message_tab = BlockTab(
            x_first_column=800,
            y_first_line=675,
            number_blocks_per_column=bot_encoded_message,
            column_direction=1,
            block_size=BLOCK_SIZE_DEFAULT
        )
        
        # Drawing bot using key & bot encoded message
        bot_using_key_tab.draw(screen)
        bot_encoded_message_tab.draw(screen)

        #Refresh the screen
        pygame.display.flip()

        # If the player've won
        if all(-1 <= value <= 1 for value in encoded_message):
            game_state = "won"

        # If bot have won
        if all(-1 <= bot_value <= 1 for bot_value in bot_encoded_message):
            game_state = "lost"
    
    # Win screen
    elif game_state == "won":

        # Updating the encoded message one last time
        private_key_tab.draw(screen)
        encoded_message_tab.draw(screen)
        bot_using_key_tab.draw(screen)
        bot_encoded_message_tab.draw(screen)

        # Displaying the decoded message
        font = pygame.font.Font(None, 30)
        decoded_text = font.render(f"Message: {decoded_message}", True, LIGHT_PURPLE_COLOR)
        if game_mode == "solo":
            screen.blit(decoded_text, (515, SCREEN_HEIGHT - 30))
        elif game_mode == "vsBot":
            screen.blit(decoded_text, (200, SCREEN_HEIGHT - 30))
            bot_decoded_text = font.render(f"Message: {bot_decoded_message}", True, LIGHT_PURPLE_COLOR)
            screen.blit(bot_decoded_text, (920, SCREEN_HEIGHT - 30))
        
        print("Last encoded message:", encoded_message)
        print("Decoded message:", decoded_message)

        # Refresh & wait
        pygame.display.flip()
        pygame.time.wait(1500)

        screen.fill(BLACK_COLOR)

        # Images & Text
        screen.blit(congrats_img, (SCREEN_WIDTH // 2 - congrats_img.get_width() // 2 + 100, -50))
        victory_text = font.render("You've decoded the message!", True, WHITE_COLOR)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 450))
        screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 550))

        # Refresh the page
        pygame.display.flip()

        # Wait few seconds to go back to the menu page
        pygame.time.wait(3000)
        game_state = "menu"
    
    # Lost screen
    elif game_state == "lost":
        screen.fill(BLACK_COLOR)
        
        # Images & Text
        screen.blit(gameover_img, (175, 25))
        lost_text = font.render("You've lost the game!", True, WHITE_COLOR)
        try_again_text = font.render("Please try again.", True, WHITE_COLOR)
        screen.blit(lost_text, (SCREEN_WIDTH // 2 - lost_text.get_width() // 2, 420))
        screen.blit(try_again_text, (SCREEN_WIDTH // 2 - try_again_text.get_width() // 2, 450))
        screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 525))

        # Refresh the page
        pygame.display.flip()

        # Wait few seconds to go back to the menu page
        pygame.time.wait(3000)
        game_state = "menu"

    # Refresh the page
    pygame.display.flip()

    clock.tick(60)

pygame.quit()