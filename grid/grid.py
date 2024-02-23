
import pygame
from ui.camera import Camera
from grid.cell import Cell

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [Cell(x, y, cell_size) for x in range(0, width, cell_size) for y in range(0, height, cell_size)]

    def get_cell(self, pos, camera):
        transformed_pos = camera.unapply(pos)
        for cell in self.cells:
            if cell.rect.collidepoint(transformed_pos):
                return cell
        return None

    def get_cell_by_id(self, id):
        for cell in self.cells:
            if cell.id == id:
                return cell
        return None

    def get_neighbors(self, cell):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                neighbor = self.get_cell_by_id((cell.id[0] + x, cell.id[1] + y))
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors
    
    def unselect_all(self):
        for cell in self.cells:
            cell.selected = False