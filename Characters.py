import pygame
from abc import ABC, abstractmethod
import math
import time
import random


class Character(ABC):
    """Abstract class for character creation. name, x, y, w, h, speed, and health are self-explanatory. Status is
    updated every frame depending on game states. Dodge is a % chance to not take damage when hit, and combat skill is
    a value that raises the characters accuracy"""
    def __init__(self, name, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.speed = speed
        self.status = status
        self.health = health
        self.dodge = dodge
        self.combat_skill = combat_skill

    @abstractmethod
    def update_status(self, teammates, enemies, player):
        """Updates the characters status depending on game state"""
        pass

    @abstractmethod
    def move(self, *args):
        """Handles the characters movement"""
        pass

    @abstractmethod
    def attack(self):
        """Allows the character to engage in combat"""
        pass

    @abstractmethod
    def die(self):
        """Checks the health of the character, and handles memory clearing"""
        pass

    @abstractmethod
    def draw(self, window):
        """Draws the character to the window. Called last after other modifiers affect the characters appearance"""
        pass


def interpolate_color(color_a, color_b, factor):
    # Interpolate between two colors
    return tuple(int(a + (b - a) * factor) for a, b in zip(color_a, color_b))


class Teammate(Character):
    """Object for the players squad members. Same variable meanings for Character except that combat skill and dodge are
    no longer static - they can increase with xp, and dodge can be modified by equipment. Role is a title that affects
    the teammates active and passive abilities. Population is a value used for game balancing - the higher your teams
    total current population, the more likely you are to see higher difficulty enemies. Different teammates contribute
    different amounts to this value. Targeted and target are used for combat targeting (duh), and is_active allows the
    player to select and give orders to specific teammates."""
    def __init__(self, name, color, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill, weapon, xp,
                 role, population, targeted, is_active=False):

        super().__init__(name, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill)
        self.color = color
        self.weapon = weapon
        self.xp = xp
        self.role = role
        self.population = population
        self.new_x = x_pos
        self.new_y = y_pos
        self.target = self
        self.is_active = is_active
        self.targeted = targeted

    def update_status(self, teammates, enemies, player):
        if self.x_pos != self.new_x or self.y_pos != self.new_y:
            self.status = 'Moving'
            self.move(self.new_x, self.new_y)
        else:
            self.status = 'Standby'

        self.calculate_target(enemies)

        if self.target != self:
            self.attack()  # Update status in this method

        if 0 < self.health < 10:
            self.status = 'Wounded'
            # Nearby Friendlies get demoralized, nearby enemies get morale buffed
        elif self.health <= 0:
            self.die()  # Give morale de-buff to friendlies and stop drawing, delete object. Award medals if earned.

    def calculate_target(self, targets):
        for target in targets:
            # Check for long range enemies
            if (self.x_pos - self.weapon.range < target.x_pos < self.x_pos + self.weapon.range
                    and self.y_pos - self.weapon.range < target.y_pos < self.y_pos + self.weapon.range):

                self.target = target

                # Check for cqc enemies
                if (self.x_pos - self.width/2 < self.target.x_pos < self.x_pos + self.width/2
                        and self.y_pos - self.height/2 < self.target.y_pos < self.y_pos + self.height/2):

                    self.status = 'Melee'
                else:
                    self.status = 'Firing'
                return
        # If no enemies, do nothing
        self.target = self

    def move(self, x_target, y_target):
        if self.status == 'Moving':
            if x_target > self.x_pos:
                self.new_x = x_target
                self.x_pos += min(self.speed, self.new_x - self.x_pos)
            elif x_target < self.x_pos:
                self.new_x = x_target
                self.x_pos -= min(self.speed, self.x_pos - self.new_x)
            if y_target > self.y_pos:
                self.new_y = y_target
                self.y_pos += min(self.speed, self.new_y - self.y_pos)
            elif y_target < self.y_pos:
                self.new_y = y_target
                self.y_pos -= min(self.speed, self.y_pos - self.new_y)

    def attack(self):
        """Gets called when self.target != self, so gotta reset it after if enemy dies"""
        if self.status == 'Melee':
            self.cqc(self.target)
        else:
            bullets_left = self.weapon.mag_size

            while bullets_left > 0:
                self.weapon.fire()
                if self.target.health < 0:
                    self.xp += 1
                    self.target = self
                    break
            self.weapon.reload()

    def cqc(self, enemy):
        """Melee over and over until one of us is dead lol"""
        while enemy.health > 0 and self.health > 0:
            # Calculate delay based on combat_skill, skewing towards 2 seconds for higher skills
            delay = random.uniform(2, 5) - (self.combat_skill / 100 * 3)
            time.sleep(max(delay, 2))  # Ensure delay doesn't go below 2 seconds

            # Check if the enemy dodges
            dodge_chance = enemy.cqc + (enemy.weapon.cqc if enemy.weapon else 0)
            if random.random() < dodge_chance:
                continue  # Enemy dodges, skip the rest of the loop

            # Calculate damage
            base_damage = int(random.randint(1, 10) * (self.combat_skill / 100))
            weapon_damage = self.weapon.attachment.damage if self.weapon and self.weapon.attachment else 0
            total_damage = base_damage + weapon_damage

            # Apply damage
            enemy.health -= total_damage

            # Check if the enemy is dead
            if enemy.health <= 0:
                self.xp += 1
                self.target = self
                break  # Enemy is dead, exit the loop
        if self.health < 10:
            self.die()

    def die(self):
        self.target = self
        pass

    def draw(self, window):
        """The oscillation here was mostly for debugging, but isn't working anymore... I'll reimplement a better visual
        indicator for the selected character at a later date."""
        base_colors = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255)}
        target_color = (255, 255, 255)  # White

        if self.is_active:
            # Get the base color for the character
            color = base_colors.get(self.color, (255, 255, 255))  # Default to white if not found

            # Use a sine wave to oscillate the factor between 0 and 1
            oscillation_speed = 10  # Adjust this value to speed up or slow down the oscillation
            time_factor = math.sin(time.time() * oscillation_speed) / 2 + 0.5  # Normalize between 0 and 1

            # Interpolate between the character's color and white
            oscillated_color = interpolate_color(color, target_color, time_factor)

            pygame.draw.rect(window, oscillated_color, (self.x_pos, self.y_pos, self.width, self.height))
        else:
            # Draw the character with their base color if not active
            color = base_colors.get(self.color, (255, 255, 255))  # Default to white if not found
            pygame.draw.rect(window, color, (self.x_pos, self.y_pos, self.width, self.height))
            

class Player(Character):
    """Object for the Player Character. Primary differences from teammate object are defaulted role and different
    movement handling (WASD)"""
    def __init__(self, name, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill, weapon, xp,
                 role='Sarge'):

        super().__init__(name, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill)
        self.weapon = weapon
        self.xp = xp
        self.role = role
        self.lives = 10
        self.target = self

    def update_status(self, teammates, enemies, player):
        pass

    def move(self, directions, screen_width, screen_height):
        for direction in directions:
            if direction == 'up':
                new_y = max(0 - self.height/2, self.y_pos - self.speed)
            elif direction == 'down':
                new_y = min(screen_height - self.height/2, self.y_pos + self.speed)
            else:
                new_y = self.y_pos
            if direction == 'left':
                new_x = max(0 - self.width/2, self.x_pos - self.speed)
            elif direction == 'right':
                new_x = min(screen_width - self.width/2, self.x_pos + self.speed)
            else:
                new_x = self.x_pos

            self.x_pos, self.y_pos = new_x, new_y

    def attack(self):
        pass

    def cqc(self, enemy):
        """Melee over and over until one of us is dead lol"""
        while enemy.health > 0 and self.health > 0:
            # Calculate delay based on combat_skill, skewing towards 2 seconds for higher skills
            delay = random.uniform(2, 5) - (self.combat_skill / 100 * 3)
            time.sleep(max(delay, 2))  # Ensure delay doesn't go below 2 seconds

            # Check if the enemy dodges
            dodge_chance = enemy.cqc + (enemy.weapon.cqc if enemy.weapon else 0)
            if random.random() < dodge_chance:
                continue  # Enemy dodges, skip the rest of the loop

            # Calculate damage
            base_damage = random.randint(1, 10) * (self.combat_skill / 100)
            weapon_damage = self.weapon.attachment.damage if self.weapon and self.weapon.attachment else 0
            total_damage = base_damage + weapon_damage

            # Apply damage
            enemy.health -= total_damage

            # Check if the enemy is dead
            if enemy.health <= 0:
                self.xp += 1
                self.target = self  # Not sure why you're setting target to self here, might want to revisit this
                break  # Enemy is dead, exit the loop
            pass
        if self.health < 10:
            self.die()

    def die(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.x_pos, self.y_pos, self.width, self.height))


class Enemy(Character):
    """Object for all enemy types in the game. Similar to teammate and player objects.
    Note: for enemy class, speed is reversed. Higher speed means more frames between moves"""
    def __init__(self, name, color, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill, weapon,
                 role):

        super().__init__(name, x_pos, y_pos, width, height, speed, status, health, dodge, combat_skill)
        self.color = color
        self.weapon = weapon
        self.role = role
        self.new_x = x_pos
        self.new_y = y_pos
        self.target = self

        # For Constant Movement Handling
        self.frame_counter = 0

    def update_status(self, enemies, teammates, player):
        self.calculate_target(enemies)

    def calculate_target(self, targets):
        for target in targets:
            if (self.x_pos - self.weapon.range < target.x_pos < self.x_pos + self.weapon.range
                    and self.y_pos - self.weapon.range < target.y_pos < self.y_pos + self.weapon.range):

                self.target = target
                return
        self.target = self

    def move(self):
        if self.status == 'Moving':
            self.frame_counter += 1
            if self.frame_counter > self.speed:
                self.x_pos -= 1
                self.frame_counter = 0
        elif self.status == 'Pinned':
            self.dodge = 0.6
            # Then draw pinned animation here
        else:
            pass

    '''If teammate or player in close range, stop moving and engage in melee until not or dead. 
    If teammate or player in long range, stop, fire, reload, then move for x ticks'''
    def attack(self):
        pass

    def cqc(self, enemy):
        """Melee over and over until one of us is dead lol"""
        while enemy.health > 0 and self.health > 0:
            # Calculate delay based on combat_skill, skewing towards 2 seconds for higher skills
            delay = random.uniform(2, 5) - (self.combat_skill / 100 * 3)
            time.sleep(max(delay, 2))  # Ensure delay doesn't go below 2 seconds

            # Check if the enemy dodges
            dodge_chance = enemy.cqc + (enemy.weapon.cqc if enemy.weapon else 0)
            if random.random() < dodge_chance:
                continue  # Enemy dodges, skip the rest of the loop

            # Calculate damage
            base_damage = random.randint(1, 10) * (self.combat_skill / 100)
            weapon_damage = self.weapon.attachment.damage if self.weapon and self.weapon.attachment else 0
            total_damage = base_damage + weapon_damage

            # Apply damage
            enemy.health -= total_damage

            # Check if the enemy is dead
            if enemy.health <= 0:
                self.xp += 1
                self.target = self  # Not sure why you're setting target to self here, might want to revisit this
                break  # Enemy is dead, exit the loop
            pass
        if self.health < 10:
            self.die()

    '''If health is critical, wail, demoralizing other enemies in range. 
    -1 health per x ticks until dead. If health <= 0, stop drawing and clear memory of enemy object'''
    def die(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 0), (self.x_pos, self.y_pos, self.width, self.height))