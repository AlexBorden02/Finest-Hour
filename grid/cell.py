
import pygame

class Cell:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.id = (x // size, y // size)
        self.cell_type = None
        self.cell_makeup = {'water': 0, 'land': 0, 'shoreline': 0}

    def get_type(self):
        return self.cell_type

    def set_type(self, type):
        self.cell_type = type

    def increment_makeup(self, subtype):
        self.cell_makeup[subtype] += 1