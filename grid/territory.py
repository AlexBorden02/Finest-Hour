import pygame

class Territory:
    def __init__(self, cells, owner):
        self.cells = cells
        self.owner = owner
        self.border_lines = []
        self.border_cells = []
        print(f'New territory created by {owner} with cells {cells}')
        self.generate_border()
    
    def get_owner(self):
        return self.owner
    
    def get_cells(self):
        return self.cells
    
    def get_border_lines(self):
        return self.border_lines
    
    def generate_border(self):
        self.border_cells = []
        # if a cell has an edge neighbor that is not owned by the same player, it is a border cell
        for cell in self.cells:
            neighbors = cell.grid.get_edge_neighbors(cell)
            for neighbor in neighbors:
                if neighbor.get_owner() != self.owner:
                    self.border_cells.append(cell)
                    break

    def expand(self, cells):
        print(f'Expanding territory by {cells}')
        for cell in cells:
            self.cells.append(cell)
            # set cell attributes
            cell.set_owner(self.owner)
            cell.set_claimed(True)
            self.generate_border() 
