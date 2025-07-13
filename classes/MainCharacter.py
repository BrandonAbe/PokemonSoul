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

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.direction_row = 1
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.direction_row = 2
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            self.direction_row = 3
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            self.direction_row = 0
            moving = True

        # Move X and check collision
        self.rect.x += dx
        self.hitbox = self.rect.inflate(0, 0)
        for npc in npc_group:
            if self.hitbox.colliderect(npc.hitbox):
                if dx > 0:  # Moving right
                    self.rect.right = npc.hitbox.left
                if dx < 0:  # Moving left
                    self.rect.left = npc.hitbox.right
                break

        # Move Y and check collision
        self.rect.y += dy
        self.hitbox = self.rect.inflate(0, 0)
        for npc in npc_group:
            if self.hitbox.colliderect(npc.hitbox):
                if dy > 0:  # Moving down
                    self.rect.bottom = npc.hitbox.top
                if dy < 0:  # Moving up
                    self.rect.top = npc.hitbox.bottom
                break
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
        self.hitbox = self.rect.inflate(0,0)
        for npc in npc_group:
            if self.hitbox.colliderect(npc.hitbox):
                self.rect = old_rect # Make sure rectangle of player does not move
                self.hitbox = self.rect.inflate(0,-10)
                break

        # Animation control
        if moving:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
        else:
            self.current_frame = 0

        self.image = self.get_sprite(self.current_frame, self.direction_row)
