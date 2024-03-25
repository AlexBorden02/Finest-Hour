
import pygame
from ui.camera import Camera
from grid.cell import Cell
from grid.territory import Territory

import random

class Grid:
    def __init__(self, width, height, cell_size, game_state_manager):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [Cell(x, y, cell_size, self) for x in range(0, width, cell_size) for y in range(0, height, cell_size)]
        self.game_state_manager = game_state_manager
        self.territories = []

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
    
    def get_edge_neighbors(self, cell):
        neighbors = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                if x == 0 or y == 0:
                    neighbor = self.get_cell_by_id((cell.id[0] + x, cell.id[1] + y))
                    if neighbor:
                        neighbors.append(neighbor)
        return neighbors

    def get_cell_size(self):
        return self.cell_size
    
    def render(self, visible_rect, screen, camera):
        if self.game_state_manager.ui_manager.get_selected_cell() is not None:
            cell = self.game_state_manager.ui_manager.get_selected_cell()
            cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
            pygame.draw.rect(screen, (0, 255, 0), (cell_pos[0], cell_pos[1], self.game_state_manager.grid.get_cell_size(), self.game_state_manager.grid.get_cell_size()), 1)

        for territory in self.territories:
            for cell in territory.border_cells:
                cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
                pygame.draw.rect(screen, (255, 0, 0), (cell_pos[0], cell_pos[1], self.game_state_manager.grid.get_cell_size(), self.game_state_manager.grid.get_cell_size()), 1)
                
    def get_claimed_cells(self):
        return [cell for cell in self.cells if cell.claimed]

    def get_random_cell(self, cell_type=None, claimed=None, border=None, owner=None):
        cells = [cell for cell in self.cells if (cell_type is None or cell.cell_type == cell_type) and (claimed is None or cell.claimed == claimed) and (border is None or cell.border == border) and (owner is None or cell.owner == owner)]
        return random.choice(cells) if cells else None

    def create_territory(self, cells, owner):
        territory = Territory(cells, owner)
        self.territories.append(territory)
        return territory
    
    def get_territory_by_cell(self, cell):
        for territory in self.territories:
            if cell in territory.cells:
                return territory
        return None
    
    def get_expansion_cells(self, territory, num_cells):
        expansion_cells = []
        # pick random cell from border cells
        for i in range(num_cells):
            cell = random.choice(territory.border_cells)
            # get neighbors
            neighbors = self.get_neighbors(cell)
            # pick random unclaimed neighbor
            unclaimed_neighbors = [neighbor for neighbor in neighbors if not neighbor.get_claimed()]
            if unclaimed_neighbors:
                expansion_cells.append(random.choice(unclaimed_neighbors))
        return expansion_cells
    