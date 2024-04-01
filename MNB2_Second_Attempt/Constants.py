import pygame


class Constant:
    def __init__(self):
        infoObject = pygame.display.Info()
        screen_width, screen_height = infoObject.current_w, infoObject.current_h
        self.screen_height = screen_height
        self.screen_width = screen_width

    def get_width(self):
        return self.screen_width

    def get_height(self):
        return self.screen_height
