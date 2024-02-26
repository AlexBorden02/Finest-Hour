
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
        self.exposed_edges = {
            'top': False,
            'right': False,
            'bottom': False,
            'left': False
        }

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

        self.check_edges(neighbours)
            
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
    
    def check_edges(self, neighbours):
        # if the cell bordering the edge of self is not claimed, set the edge to exposed
        for neighbour in neighbours:
            if neighbour.id[0] == self.id[0] - 1:
                self.exposed_edges['left'] = not neighbour.claimed
            if neighbour.id[0] == self.id[0] + 1:
                self.exposed_edges['right'] = not neighbour.claimed
            if neighbour.id[1] == self.id[1] - 1:
                self.exposed_edges['top'] = not neighbour.claimed
            if neighbour.id[1] == self.id[1] + 1:
                self.exposed_edges['bottom'] = not neighbour.claimed


        return self.exposed_edges