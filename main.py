import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BG_COLOR = (192, 192, 192) # Background color

# Frame rate
FPS = 60

# Main character class
class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, sprite_width, sprite_height):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

        self.direction_row = 0 #0 = down, 1 = left, 2 = right, 3 = up
        self.current_frame = 0
        self.frame_count = 4 # Because there are 4 columns in our image

        self.animation_speed = 0.15 # Fractional animation speed for smooth animations,
                                    # regardless of your FPS
        self.animation_timer = 0

        self.image = self.get_sprite(self.current_frame, self.direction_row)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1

    def get_sprite(self, col, row):
        rect = pygame.Rect(
        col * self.sprite_width,
        row * self.sprite_height,
        self.sprite_width,
        self.sprite_height
        )
        return self.sprite_sheet.subsurface(rect).copy()


    def set_sprite(self, col, row):
        self.current_sprite_idx = (col, row)
        self.image = self.get_sprite(col, row)

    def update(self, keys):
        moving = False # Booleans can be True or False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction_row = 1
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction_row = 2
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction_row = 3
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction_row = 0
            moving = True

        # Keep character on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if moving == True:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
        else:
            self.current_frame = 0 # Reset to first frame when idle

        # Update sprite image of main character
        self.image = self.get_sprite(self.current_frame, self.direction_row)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Soul by Lil' Dave and BrandonAbe")

# Create clock for FPS
clock = pygame.time.Clock()

# Create main character sprite
character_image_path = os.path.join("assets", "main_character.png") # assets/main_character.png
main_character = MainCharacter(
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2,
    character_image_path,
    sprite_width=32,
    sprite_height=48
)

# Sprite group for easy updates/draws
all_sprites = pygame.sprite.Group()
all_sprites.add(main_character)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    screen.fill(BG_COLOR)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
