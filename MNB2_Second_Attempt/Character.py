import pygame
from Constants import Constant
from Bullets import Bullet

class Sarge(pygame.sprite.Sprite):
    def __init__(self):
        c = Constant()
        super(Sarge, self).__init__()
        self.image = pygame.image.load('Sarge_Refined.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1, self.image.get_height() * 1))
        self.rect = self.image.get_rect()
        self.rect.x = c.screen_width // 2
        self.rect.y = c.screen_height - self.rect.height
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 3
        self.bullet_group = pygame.sprite.Group()


    def update(self, directions):
        c = Constant()
        self.rect.x += self.vel_x
        if self.rect.x >= c.get_width() - self.image.get_width() or self.rect.x <= 0:
            self.rect.x -= self.vel_x
        self.rect.y += self.vel_y

        if directions:
            bullet = Bullet()
            self.bullet_group.add(bullet)
            if len(self.bullet_group) > 50:
                first_sprite = next(iter(self.bullet_group))  # Get the first sprite
                self.bullet_group.remove(first_sprite)

        self.bullet_group.update(directions)


class Target(pygame.sprite.Sprite):
    def __init__(self):
        c = Constant()
        super(Target, self).__init__()
        self.image = pygame.image.load('Volkssturn_Refined.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1, self.image.get_height() * 1))
        self.rect = self.image.get_rect()
        self.rect.x = c.screen_width // 2
        self.rect.y = c.screen_height // 2
        self.hp = 100
