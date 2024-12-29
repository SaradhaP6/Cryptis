import pygame
import os
from keys import generate_private_key, generate_public_key
from messages import generate_message, message_to_ternary, ternary_to_message, encode_message
from block import BlockTab
import time


### Constants
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 750
FPS = 60
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_PURPLE_COLOR = (224, 170, 255)
DARK_PURPLE_COLOR = (123, 44, 191)
BLOCK_SIZE_DEFAULT = (50, 10)

### pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cryptris by Saradha")
clock = pygame.time.Clock()
running = True

### Elements for menu
game_state = "menu"
# Button
button_color = LIGHT_PURPLE_COLOR
button_hover_color = DARK_PURPLE_COLOR
button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100//2, 500, 100, 50)
# Logo
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
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
# Text on menu page
font = pygame.font.Font(None, 30)
title_text1 = font.render("by Saradha", True, WHITE_COLOR)
title_text2 = font.render("Based on the game, Cryptris,", True, WHITE_COLOR)
title_text3 = font.render("developped by Digital Cuisine & Inria", True, WHITE_COLOR)

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


def initialize_game():
    global private_key, public_key, message, ternary_message, encoded_message, private_key_tab, encoded_message_tab, start_time, decoded_message
    private_key = generate_private_key(8)
    public_key = generate_public_key(private_key)
    message = generate_message(8)
    ternary_message = message_to_ternary(message)
    encoded_message = encode_message(ternary_message, public_key)

    private_key_tab = BlockTab(
        x_first_column=100,
        y_first_line=75,
        number_blocks_per_column=private_key,
        column_direction=-1,
        block_size=BLOCK_SIZE_DEFAULT
    )

    encoded_message_tab = BlockTab(
        x_first_column=100,
        y_first_line=700,
        number_blocks_per_column=encoded_message,
        column_direction=1,
        block_size=BLOCK_SIZE_DEFAULT
    )
    print("New game initialized")
    decoded_message = ternary_to_message(encoded_message)
    start_time = time.time()



"""
Main loop
"""
while running:

    clock.tick(FPS)

    # Timer  
    if game_state == "playing" and start_time:
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            game_state = "lost"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN :
            if button_rect.collidepoint(event.pos):
                initialize_game()
                print("Private Key:", private_key)
                print("Initial Message:", message)
                print("Initial Ternary Message:", ternary_message)
                print("Encoded Message:", encoded_message)
                game_state = "playing"
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
        if button_rect.collidepoint(mouse_pos):
            # If the player is hovering on the button
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 370))
            screen.blit(title_text3, (SCREEN_WIDTH // 2 - title_text3.get_width() // 2, 400))

            # Play button
            pygame.draw.rect(screen, button_hover_color, button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
        else:
            # If the player's mouse is not on the button
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_img, (SCREEN_WIDTH//2 - logo_img.get_width()//2, 180))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 300))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 370))
            screen.blit(title_text3, (SCREEN_WIDTH // 2 - title_text3.get_width() // 2, 400))

            # Play button
            pygame.draw.rect(screen, button_color, button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
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
        remaining_time = max(0, time_limit - (time.time() - start_time))
        font = pygame.font.Font(None, 30)
        timer_text = font.render(f"Time left: {int(remaining_time)}s", True, LIGHT_PURPLE_COLOR)
        screen.blit(timer_text, (10, 10))

        # Update of Private key's blocks
        private_key_tab = BlockTab(
            x_first_column=100,
            y_first_line=75,
            number_blocks_per_column=private_key,
            column_direction=-1,
            block_size=blocks_size
        )

        # Displaying the decoded message
        font = pygame.font.Font(None, 30)
        decoded_text = font.render(f"Message: {decoded_message}", True, LIGHT_PURPLE_COLOR)
        screen.blit(decoded_text, (225, SCREEN_HEIGHT - 30))

        # Displaying the key to use to play
        screen.blit(key_use_img, (565, SCREEN_HEIGHT//2 - key_use_img.get_height()//2))

        # Drawing the blocks for the private key and the encoded message
        private_key_tab.draw(screen)
        encoded_message_tab.draw(screen)

        # Falling key: Updating encoded message value
        if key_falling:
            for i in range(len(private_key)):
                encoded_message[i] += private_key[i]
            # Updating of the encoded message's blocks
            encoded_message_tab = BlockTab(
                x_first_column=100,
                y_first_line=700,
                number_blocks_per_column=encoded_message,
                column_direction=1,
                block_size=blocks_size
            )
            decoded_message = ternary_to_message(encoded_message)
            key_falling = False
            
        encoded_message_tab.draw(screen)
        pygame.display.flip()

        # If the player won
        if all(-1 <= value <= 1 for value in encoded_message):
            game_state = "won"
    
    # Win screen
    elif game_state == "won":

        # Updating the encoded message one last time
        private_key_tab.draw(screen)
        encoded_message_tab.draw(screen)

        # Displaying the decoded message
        font = pygame.font.Font(None, 30)
        decoded_text = font.render(f"Message: {decoded_message}", True, LIGHT_PURPLE_COLOR)
        screen.blit(decoded_text, (225, SCREEN_HEIGHT - 30))
        
        print("Last encoded message:", encoded_message)
        print("Decoded message:", decoded_message)

        # Refresh & wait
        pygame.display.flip()
        pygame.time.wait(1500)

        screen.fill(BLACK_COLOR)

        # Images & Text
        screen.blit(congrats_img, (125, -50))
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