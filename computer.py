import pygame

class Computer:
    def __init__(self, name=None, color=(255, 255, 255)):
        self.computer_id = id(self)
        self.name = name
        self.color = color
        self.claimed_cells = []

    def claim_cell(self, cell):
        cell.set_claimed(True)
        self.claimed_cells.append(cell)
        cell.set_owner(self.computer_id)

    def claim_cells(self, cells):
        for cell in cells:
            self.claim_cell(cell)

    def unclaim_cell(self, cell):
        cell.unclaim()
        self.claimed_cells.remove(cell)

    def get_computer_id(self):
        return self.computer_id
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_claimed_cells(self):
        return self.claimed_cells
