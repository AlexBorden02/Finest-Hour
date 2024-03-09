
import pygame

class Cell:
    def __init__(self, x, y, size, grid):
        self.rect = pygame.Rect(x, y, size, size)
        self.id = (x // size, y // size)
        self.cell_type = None
        self.cell_makeup = {'water': 0, 'land': 0, 'shoreline': 0}
        self.claimed = False
        self.border = False
        self.grid = grid
        self.owner = None

    def get_type(self):
        return self.cell_type

    def set_type(self, type):
        self.cell_type = type

    def increment_makeup(self, subtype):
        self.cell_makeup[subtype] += 1

    def get_makeup(self):
        return self.cell_makeup
    
    def set_makeup(self, makeup):
        self.cell_makeup = makeup
    
    def get_id(self):
        return self.id
    
    def get_rect(self):
        return self.rect
    
    def get_claimed(self):
        return self.claimed
    
    def __str__(self):
        return f'Cell: {self.id}: Claimed:{self.claimed} Owner: {self.owner}'
    
    def set_claimed(self, claimed):
        self.claimed = claimed
        return self.claimed
    
    def get_owner(self):
        return self.owner
    
    def set_owner(self, owner):
        self.owner = owner
        return self.owner
    
    def unclaim(self):
        self.set_claimed(False)
        self.set_owner(None)