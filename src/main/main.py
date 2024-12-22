import pygame
import os
from keys import generate_private_key, generate_public_key
from messages import generate_message, message_to_ternary, encode_message, decode_message_private_key
from block import Block
import time

### Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_PURPLE_COLOR = (142, 68, 173)
DARK_PURPLE_COLOR = (74, 35, 90)

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
button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100//2, 350, 100, 50)
# Logo
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
logo_path = os.path.join(current_dir, "../img/logo.png")
logo_path = os.path.abspath(logo_path)
try:
    logo = pygame.image.load(logo_path)
    logo_menu = pygame.transform.scale_by(logo, 0.7)
    logo_playing = pygame.transform.scale_by(logo, 0.4)
except pygame.error as e:
    print("Erreur lors du chargement du logo :", e)
    pygame.quit()
    exit()
# Text
font = pygame.font.Font(None, 30)
title_text1 = font.render("by Saradha", True, WHITE_COLOR)
title_text2 = font.render("Based on the game, Cryptris, developped by Digital Cuisine & Inria", True, WHITE_COLOR)

### Elements for the winning page


### Elements for the loosing page


"""
Main loop
"""
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK_COLOR)

    if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
            if button_rect.collidepoint(event.pos):
                game_state = "playing"

    if game_state == "menu":
        # Player is on the main menu
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            # If the player is hovering on the button
            screen.fill(BLACK_COLOR)

            # Logo & Text
            screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 150))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 280))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 310))

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
            screen.blit(logo_menu, (SCREEN_WIDTH//2 - logo_menu.get_width()//2, 150))
            screen.blit(title_text1, (SCREEN_WIDTH // 2 - title_text1.get_width() // 2, 280))
            screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 310))

            # Play button
            pygame.draw.rect(screen, button_color, button_rect)
            font = pygame.font.Font(None, 30)
            text_surface = font.render("Start", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
    
    elif game_state == "playing":
        # Player is playing
        print("Player is playing...")

        # Tests clés
        private_key = generate_private_key(8)
        public_key = generate_public_key(private_key)
        print(private_key)
        print(public_key)
        
        # Tests message
        message = generate_message(8)
        print(message)
        ternary_message = message_to_ternary(message)
        print(ternary_message)
        encoded_message = encode_message(ternary_message, public_key)
        print(encoded_message)
        decoded_message = decode_message_private_key(encoded_message, private_key)
        print(decoded_message)
        
    elif game_state == "won":
        # Joueur a gagné : on affiche "Congrats !" et on met game_state = "menu"
        print("Winner !")
    
    elif game_state == "lost":
        # Joueur a perdu : on affiche "Dommage ! Retentez votre chance." et on met game_state = "menu"
        print("Looser !")

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()