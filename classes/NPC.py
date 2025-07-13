import pygame
import settings

# NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, sprite_width, sprite_height):
        super().__init__()
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

        self.current_frame = 0
        self.frame_count = 1  # If using single frame for now
        self.direction_row = 0

        self.image = self.get_sprite(self.current_frame, self.direction_row)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(0,0) # Adjust hitbox

    def get_sprite(self, col, row):
        rect = pygame.Rect(
            col * self.sprite_width,
            row * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )
        return self.sprite_sheet.subsurface(rect).copy()

    def update(self, *args, **kwargs):
        pass  # For now, the NPC remains static
