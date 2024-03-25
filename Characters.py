import pygame
#for abstract classes
from abc import ABC, abstractmethod

import math
import time

#Abstract class for character creation. name, x, y, w, h, speed, health are self explanatory. status would be things like
#'pinned' or 'reloading' or 'shooting' or 'fleeing' or 'dead'. Dodge is a % chance to not take damage
#when hit, and combat skill is a value that raises your weapons accuracy
class Character(ABC):
    def __init__(self, name, xPos, yPos, width, height, speed, status, health, dodge, combat_skill):
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.speed = speed
        self.status = status
        self.health = health
        self.dodge = dodge
        self.combat_skill = combat_skill
    def _ensure_attributes(self):
        required_attributes = ["name", "xPos", "yPos", "width", "height", "speed", "status", "health", "dodge", "combat_skill"]
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f"{type(self).__name__} is missing required attribute: {attr}")

    @abstractmethod
    def move(self, *args):
        pass

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def draw(self, window):
        pass


class Teammate(Character):
    def __init__(self, name, color, xPos, yPos, width, height, speed, status, health, dodge, combat_skill, weapon, XP, role, popCont, isActive):
        super().__init__(name, xPos, yPos, width, height, speed, status, health, dodge, combat_skill)
        self.color = color
        self.weapon = weapon
        self.XP = XP
        self.role = role
        self.popCont = popCont
        self.targetX = xPos
        self.targetY = yPos
        self.isActive = False

    def move(self, x_target, y_target):
        if x_target > self.xPos:
            self.targetX = x_target
            self.xPos += min(self.speed, self.targetX - self.xPos)
        elif x_target < self.xPos:
            self.targetX = x_target
            self.xPos -= min(self.speed, self.xPos - self.targetX)
        if y_target > self.yPos:
            self.targetY = y_target
            self.yPos += min(self.speed, self.targetY - self.yPos)
        elif y_target < self.yPos:
            self.targetY = y_target
            self.yPos -= min(self.speed, self.yPos - self.targetY)

    def attack(self):
        pass

    def die(self):
        pass

    def interpolate_color(self, colorA, colorB, factor):
        # Interpolate between two colors
        return tuple(int(a + (b - a) * factor) for a, b in zip(colorA, colorB))

    def draw(self, window):
        base_colors = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255)}
        target_color = (255, 255, 255)  # White

        if self.isActive:
            # Get the base color for the character
            color = base_colors.get(self.color, (255, 255, 255))  # Default to white if not found

            # Use a sine wave to oscillate the factor between 0 and 1
            oscillation_speed = 10  # Adjust this value to speed up or slow down the oscillation
            time_factor = math.sin(time.time() * oscillation_speed) / 2 + 0.5  # Normalize between 0 and 1

            # Interpolate between the character's color and white
            oscillated_color = self.interpolate_color(color, target_color, time_factor)

            pygame.draw.rect(window, oscillated_color, (self.xPos, self.yPos, self.width, self.height))
        else:
            # Draw the character with their base color if not active
            color = base_colors.get(self.color, (255, 255, 255))  # Default to white if not found
            pygame.draw.rect(window, color, (self.xPos, self.yPos, self.width, self.height))

class Player(Character):
    def __init__(self, name, xPos, yPos, width, height, speed, status, health, dodge, combat_skill, weapon, XP, role = 'Sarge'):
        super().__init__(name, xPos, yPos, width, height, speed, status, health, dodge, combat_skill)
        self.weapon = weapon
        self.XP = XP
        self.role = role

    def move(self, directions, screen_width, screen_height):
        for direction in directions:
            if direction == 'up':
                new_y = max(0 - self.height/2, self.yPos - self.speed)
            elif direction == 'down':
                new_y = min(screen_height - self.height/2, self.yPos + self.speed)
            else:
                new_y = self.yPos
            if direction == 'left':
                new_x = max(0 - self.width/2, self.xPos - self.speed)
            elif direction == 'right':
                new_x = min(screen_width - self.width/2, self.xPos + self.speed)
            else:
                new_x = self.xPos

            self.xPos, self.yPos = new_x, new_y

    def attack(self):
        pass

    def die(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.xPos, self.yPos, self.width, self.height))
