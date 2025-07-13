import pygame
import settings

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
        self.speed = 2

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

    def update(self, keys, npc_group):
        old_rect = self.rect.copy()  # Save current position
        moving = False

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
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT

        # Check collision with NPCs
        if pygame.sprite.spritecollideany(self, npc_group):
            self.rect = old_rect  # Revert to previous position

        # Animation control
        if moving:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
        else:
            self.current_frame = 0

        self.image = self.get_sprite(self.current_frame, self.direction_row)
