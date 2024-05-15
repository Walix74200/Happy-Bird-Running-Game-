import pygame
import random

largeur, hauteur = 900, 900

class Gemme(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gemme.png").convert_alpha()  # Remplacez avec le chemin de votre image de gemme
        self.rect = self.image.get_rect()
        self.rect.x = largeur
        self.rect.y = random.randint(100, hauteur - 100)
        self.velocity_x = -5

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right < 0:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("projectile1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 10

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.left > largeur:
            self.kill()