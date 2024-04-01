import pygame
from Constants import Constant
import random as rand


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        c = Constant()
        super(Bullet, self).__init__()
        self.image = pygame.image.load('Bullet_Refined.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.5, self.image.get_height() * 0.5))
        self.rect = self.image.get_rect()
        self.rect.x = c.screen_width // 2
        self.rect.y = c.screen_height // 2
        self.accuracy = 50
        self.fired = False

    def update(self, directions):
        if directions and not self.fired:
            self.rect.x = rand.randrange(directions[0] - self.image.get_width()//2 - self.accuracy, directions[0] - self.image.get_width()//2 + self.accuracy)
            self.rect.y = rand.randrange(directions[1] - self.image.get_height()//2 - self.accuracy, directions[1] - self.image.get_height()//2 + self.accuracy)
            self.fired = True


