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

    def move_WASD(self, directions, screen_width, screen_height):
        for direction in directions:
            if direction == 'up':
                new_y = max(self.height // 2, self.y - self.speed)
            elif direction == 'down':
                new_y = min(screen_height - self.height // 2, self.y + self.speed)
            else:
                new_y = self.y

            if direction == 'left':
                new_x = max(self.width // 2, self.x - self.speed)
            elif direction == 'right':
                new_x = min(screen_width - self.width // 2, self.x + self.speed)
            else:
                new_x = self.x

            self.x, self.y = new_x, new_y


