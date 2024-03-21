# Character.py
import pygame

class Character:
    def __init__(self, name, x, y, width, height, color, speed, isActive):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.targetX = x
        self.targetY = y
        self.isActive = isActive

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move_towards_target(self):
        if self.targetX > self.x:
            self.x += min(self.speed, self.targetX - self.x)
        elif self.targetX < self.x:
            self.x -= min(self.speed, self.x - self.targetX)

        if self.targetY > self.y:
            self.y += min(self.speed, self.targetY - self.y)
        elif self.targetY < self.y:
            self.y -= min(self.speed, self.y - self.targetY)

    def move_WASD(self, direction):
        if direction == 'up':
            self.y -= self.speed
        elif direction == 'down':
            self.y += self.speed
        elif direction == 'left':
            self.x -= self.speed
        elif direction == 'right':
            self.x += self.speed

