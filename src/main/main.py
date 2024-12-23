import pygame
import os
from keys import generate_private_key, generate_public_key
from messages import generate_message, message_to_ternary, encode_message, decode_message_private_key
from block import BlockTab
import time


### Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
FPS = 60
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
#LIGHT_PURPLE_COLOR = (142, 68, 173)
#DARK_PURPLE_COLOR = (74, 35, 90)
LIGHT_PURPLE_COLOR = (224, 170, 255)
DARK_PURPLE_COLOR = (123, 44, 191)
BLOCK_SIZE = (50, 10)

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
congrats_path = os.path.join(current_dir, "../img/congrats.png")
congrats_path = os.path.abspath(congrats_path)
try:
    logo = pygame.image.load(logo_path)
    logo_menu = pygame.transform.scale_by(logo, 0.6)
    logo_playing = pygame.transform.scale_by(logo, 0.3)
except pygame.error as e:
    print("Error when loading the logo image :", e)
    logo_menu = pygame.Surface((100, 50))
    logo_menu.fill(BLACK_COLOR)
    logo_playing = pygame.Surface((50, 25))
    logo_playing.fill(BLACK_COLOR)
# Text
font = pygame.font.Font(None, 30)
title_text1 = font.render("by Saradha", True, WHITE_COLOR)
title_text2 = font.render("Based on the game, Cryptris,", True, WHITE_COLOR)
title_text3 = font.render("developped by Digital Cuisine & Inria", True, WHITE_COLOR)

### Elements for the winning page
congrats_path = os.path.join(current_dir, "../img/congrats.png")
congrats_path = os.path.abspath(congrats_path)
try:
    congrats_img = pygame.image.load(congrats_path)
except pygame.error as e:
    print("Error when loading the congrats image :", e)
    congrats_img = pygame.Surface((100, 50))
    congrats_img.fill(BLACK_COLOR)

### Elements for the loosing page


### Elements for the game
private_key = []
public_key = []
encoded_message = []
rotation_index = 0
sign_inversion = 1
key_falling = False
private_key_tab = None
encoded_message_tab = None


def initialize_game():
    global private_key, public_key, encoded_message, private_key_tab, encoded_message_tab
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
        block_size=BLOCK_SIZE
    )

    encoded_message_tab = BlockTab(
        x_first_column=100,
        y_first_line=700,
        number_blocks_per_column=encoded_message,
        column_direction=1,
        block_size=BLOCK_SIZE
    )
    print("New game initialized")


"""
Main loop
"""
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN :
            if button_rect.collidepoint(event.pos):
                initialize_game()
                print("Private Key:", private_key)
                print("Encoded Message:", encoded_message)
                game_state = "playing"
        elif game_state == "playing" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                private_key = private_key[1:] + private_key[:1]  # Rotate left
            elif event.key == pygame.K_RIGHT:
                private_key = private_key[-1:] + private_key[:-1]  # Rotate right
            elif event.key == pygame.K_UP:
                sign_inversion *= -1
                private_key = [-val for val in private_key]  # Flip sign
            elif event.key == pygame.K_RETURN:
                key_falling = True  # Trigger the "drop" action
    
    screen.fill(BLACK_COLOR)

    # Main menu
    if game_state == "menu":

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            # If the player is hovering on the button
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 180))
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
            screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 180))
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

        # Background for the playing screen
        screen.fill(BLACK_COLOR)
        
        # Logo for the playing screen
        screen.blit(logo_playing, (SCREEN_WIDTH//2 - logo_playing.get_width()//2, 750))

        # Update of Private key's blocks
        private_key_tab = BlockTab(
            x_first_column=100,
            y_first_line=75,
            number_blocks_per_column=private_key,
            column_direction=-1,
            block_size=BLOCK_SIZE
        )

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
                block_size=BLOCK_SIZE
            )
            key_falling = False
            
        encoded_message_tab.draw(screen)
        pygame.display.flip()

        # If the player won
        if all(-1 <= value <= 1 for value in encoded_message):
            game_state = "won"
    
    # Win screen
    elif game_state == "won":

        # Updating the encoded message one last time
        encoded_message_tab.draw(screen)
        screen.blit(logo_playing, (SCREEN_WIDTH//2 - logo_playing.get_width()//2, 750))
        pygame.display.flip()
        pygame.time.wait(1000)

        screen.fill(BLACK_COLOR)

        # Logo & Text
        screen.blit(congrats_img, (SCREEN_WIDTH//2 - congrats_img.get_width()//2, 100))
        victory_text = font.render("You've decoded the message!", True, WHITE_COLOR)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 500))
        # Refresh the page
        pygame.display.flip()

        # Wait few seconds to go back to the menu page
        pygame.time.wait(10000)
        game_state = "menu"
    
    # Lost screen
    elif game_state == "lost":
        
        screen.fill(BLACK_COLOR)
        
        # Logo & Text
        screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 180))
        victory_text = font.render("Sorry, you've lost. Try again !", True, WHITE_COLOR)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2))
        # Refresh the page
        pygame.display.flip()

        # Wait few seconds to go back to the menu page
        pygame.time.wait(2000)
        game_state = "menu"

    # Refresh the page
    pygame.display.flip()

    clock.tick(60)

pygame.quit()