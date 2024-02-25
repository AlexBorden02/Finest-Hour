
import pygame

class Cell:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.id = (x // size, y // size)
        self.cell_type = None
        self.cell_makeup = {'water': 0, 'land': 0, 'shoreline': 0}
        self.modified = False

    def get_type(self):
        return self.cell_type

    def set_type(self, type):
        self.cell_type = type

    def increment_makeup(self, subtype):
        self.cell_makeup[subtype] += 1

    def get_makeup(self):
        return self.cell_makeup
    
    def get_id(self):
        return self.id
    
    def get_rect(self):
        return self.rect
    
    def get_modified(self):
        return self.modified
    
    def set_modified(self, modified):
        self.modified = modified
        