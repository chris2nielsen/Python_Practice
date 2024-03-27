import time
import pygame
clock = pygame.time.Clock()


class Weapon:
    def __init__(self, name, damage, accuracy, range, weight, mag_size, fire_rate, reload_time, cqc, attachment):
        self.name = name
        self.damage = int(damage)
        self.accuracy = float(accuracy)
        self.range = int(range)
        self.weight = float(weight)
        self.mag_size = int(mag_size)
        self.fire_rate = float(fire_rate)
        self.reload_time = float(fire_rate)
        self.cqc = float(cqc)
        self.attachment = attachment

    def use_attachment(self):
        # if attachment.ability != 'none'
        pass

    def fire(self):
        # enemy gets shot at by a single bullet
        clock.tick(self.fire_rate)
        pass


class Attachment():
    def __init__(self, name, damage, accuracy, range, weight, mag_size, fire_rate, reload_time, cqc, ability):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.range = range
        self.weight = weight
        self.mag_size = mag_size
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.cqc = cqc
        self.ability = ability
