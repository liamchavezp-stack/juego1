import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 16))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
