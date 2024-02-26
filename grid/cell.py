
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
        return f'Cell: {self.id}: {self.cell_type} {self.claimed} {self.border} {self.owner}'
    
    def set_claimed(self, claimed):
        self.claimed = claimed
        self.check_border()
        return self.claimed
    
    def check_border(self, recursive=False):
        neighbours = self.grid.get_edge_neighbors(self)
        # if any neighbour is not claimed, set border to True
        self.border = any([not neighbour.claimed for neighbour in neighbours]) & self.claimed
        print(f'Cell: {self.id} Neighbours: {[neighbour.claimed for neighbour in neighbours]} Border: {self.border}')

        if not recursive:
            for neighbour in neighbours:
                neighbour.check_border(True)

        return self.border
    
    def get_owner(self):
        return self.owner
    
    def set_owner(self, owner):
        self.owner = owner
        return self.owner
    