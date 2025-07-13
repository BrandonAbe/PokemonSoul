import pygame
import sys
import os
import time
import settings
from classes.MainCharacter import MainCharacter
from classes.NPC import NPC 

# Initialize pygame
pygame.init()

# Setup display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Soul by Lil' Dave and BrandonAbe")

# Create clock for FPS
clock = pygame.time.Clock()

# Font for menu
font = pygame.font.SysFont(None, 48)

# Menu options
menu_options = ["Play", "Settings", "Quit"] #List in python
selected_index = 0

# Game state
state = "menu"

# Create main character sprite
character_image_path = os.path.join("assets", "main_character.png") # assets/main_character.png
main_character = MainCharacter(
    settings.SCREEN_WIDTH // 2,
    settings.SCREEN_HEIGHT // 2,
    character_image_path,
    sprite_width=32,
    sprite_height=48
)

# Create NPC sprite
rival_image_path = os.path.join("assets", "rival_character.png") # assets/main_character.png
rival = NPC(
    settings.SCREEN_WIDTH // 2 + 100,
    settings.SCREEN_HEIGHT // 2,
    rival_image_path,
    sprite_width=32,
    sprite_height=48
)

# Sprite group for easy updates/draws
all_sprites = pygame.sprite.Group()
all_sprites.add(main_character)
all_sprites.add(rival)

npc_group = pygame.sprite.Group()
npc_group.add(rival)


# Main game loop
running = True
while running:
    clock.tick(settings.FPS)
    screen.fill(settings.BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if state == "menu":
        if event.type == pygame.KEYDOWN: # Check if keyboard is pressed
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_options) # Wraps around
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                selected_option = menu_options[selected_index]
                if selected_option == "Play":
                    state = "play"
                elif selected_option == "Settings":
                    state = "settings"
                elif selected_option == "Quit":
                    state = "quit"
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(menu_options):
                text_surface = font.render(option, True, settings.WHITE)
                text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH//2, 250 + i*60))
                if text_rect.collidepoint(mouse_pos):
                    if option == "Play":
                        state = "play"
                    elif option == "Settings":
                        state = "settings"
                    elif option == "Quit":
                        state = "quit"
                        running = False

    # Render menu
    if state == "menu":
        for i, option in enumerate(menu_options):
            color = settings.GREY if i == selected_index else settings.WHITE
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH//2, 250 + i*60))
            screen.blit(text_surface, text_rect)

    # Render game
    elif state == "play":
        keys = pygame.key.get_pressed()
        main_character.update(keys, npc_group)  # Player needs npc_group for collision
        npc_group.update(keys)                  # NPCs can animate if desired
        all_sprites.draw(screen)

        # Press ESC to return to menu
        if keys[pygame.K_ESCAPE]:
            state = "menu"

    pygame.display.flip()

pygame.quit()
sys.exit()