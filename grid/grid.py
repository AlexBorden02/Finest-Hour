
import pygame
from ui.camera import Camera
from grid.cell import Cell

class Grid:
    def __init__(self, width, height, cell_size, game_state_manager):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [Cell(x, y, cell_size) for x in range(0, width, cell_size) for y in range(0, height, cell_size)]
        self.game_state_manager = game_state_manager

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

    def get_cell_size(self):
        return self.cell_size
    
    def render(self, visible_rect, screen, camera):
        if self.game_state_manager.ui_manager.get_selected_cell() is not None:
            cell = self.game_state_manager.ui_manager.get_selected_cell()
            cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
            pygame.draw.rect(screen, (0, 255, 0), (cell_pos[0], cell_pos[1], self.game_state_manager.grid.get_cell_size(), self.game_state_manager.grid.get_cell_size()), 1)

        modified_cells = self.get_modified_cells()
        for cell in modified_cells:
            cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
            pygame.draw.rect(screen, (255, 0, 0), (cell_pos[0], cell_pos[1], self.game_state_manager.grid.get_cell_size(), self.game_state_manager.grid.get_cell_size()), 1)
        
    def get_modified_cells(self):
        return [cell for cell in self.cells if cell.modified]
    
    def clump_modified_cells(self):
        visited = set()
        clumps = []

        def dfs(cell):
            if cell in visited or not cell.modified:
                return []
            visited.add(cell)
            clump = [cell]
            for neighbor in self.get_neighbors(cell):
                clump.extend(dfs(neighbor))
            return clump

        for cell in self.cells:
            if cell.modified and cell not in visited:
                clumps.append(dfs(cell))

        return clumps