# Character.py
import pygame

class Character:
    def __init__(self, name, xPos, yPos, width, height, color, speed, isActive):
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.targetX = xPos
        self.targetY = yPos
        self.isActive = isActive

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.xPos, self.yPos, self.width, self.height))

    def move_towards_target(self):
        if self.targetX > self.xPos:
            self.xPos += min(self.speed, self.targetX - self.xPos)
        elif self.targetX < self.xPos:
            self.xPos -= min(self.speed, self.xPos - self.targetX)

        if self.targetY > self.yPos:
            self.yPos += min(self.speed, self.targetY - self.yPos)
        elif self.targetY < self.yPos:
            self.yPos -= min(self.speed, self.yPos - self.targetY)

    def move_WASD(self, directions, screen_width, screen_height):
        for direction in directions:
            if direction == 'up':
                new_y = max(0, self.yPos - self.speed)
            elif direction == 'down':
                new_y = min(screen_height - self.height, self.yPos + self.speed)
            else:
                new_y = self.yPos
            if direction == 'left':
                new_x = max(0, self.xPos - self.speed)
            elif direction == 'right':
                new_x = min(screen_width - self.width, self.xPos + self.speed)
            else:
                new_x = self.xPos

            self.xPos, self.yPos = new_x, new_y


