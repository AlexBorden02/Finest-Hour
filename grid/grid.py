
import pygame
from ui.camera import Camera
from grid.cell import Cell

import random

class Grid:
    def __init__(self, width, height, cell_size, game_state_manager):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [Cell(x, y, cell_size, self) for x in range(0, width, cell_size) for y in range(0, height, cell_size)]
        self.game_state_manager = game_state_manager
        self.clump_cache = {}

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
            clump = self.game_state_manager.ui_manager.get_selected_clump()
            # if length of clump is greater than 1, draw all cells in clump
            if clump and len(clump) > 1:
                for cell in clump:
                    cell_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
                    pygame.draw.rect(screen, (255, 0, 0), (cell_pos[0], cell_pos[1], self.game_state_manager.grid.get_cell_size(), self.game_state_manager.grid.get_cell_size()), 1)

        player_cells = self.game_state_manager.player.get_claimed_cells()
        for cell in player_cells:
            cell_color = self.game_state_manager.player.get_color()
            if cell.border:
                # draw exposed edges
                for edge, exposed in cell.exposed_edges.items():
                    if exposed:
                        edge_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
                        if edge == 'top':
                            pygame.draw.line(screen, cell_color, edge_pos, (edge_pos[0] + self.cell_size - 1, edge_pos[1]), 1)
                        elif edge == 'right':
                            pygame.draw.line(screen, cell_color, (edge_pos[0] + self.cell_size - 1, edge_pos[1]), (edge_pos[0] + self.cell_size - 1, edge_pos[1] + self.cell_size - 1), 1)
                        elif edge == 'bottom':
                            pygame.draw.line(screen, cell_color, (edge_pos[0], edge_pos[1] + self.cell_size - 1), (edge_pos[0] + self.cell_size - 1, edge_pos[1] + self.cell_size - 1), 1)
                        elif edge == 'left':
                            pygame.draw.line(screen, cell_color, edge_pos, (edge_pos[0], edge_pos[1] + self.cell_size - 1), 1)

        for npc in self.game_state_manager.npcs:
            npc_cells = npc.get_claimed_cells()
            for cell in npc_cells:
                cell_color = npc.get_color()
                if cell.border:
                    # draw exposed edges
                    for edge, exposed in cell.exposed_edges.items():
                        if exposed:
                            edge_pos = (cell.rect.x - visible_rect.x, cell.rect.y - visible_rect.y)
                            if edge == 'top':
                                pygame.draw.line(screen, cell_color, edge_pos, (edge_pos[0] + self.cell_size - 1, edge_pos[1]), 1)
                            elif edge == 'right':
                                pygame.draw.line(screen, cell_color, (edge_pos[0] + self.cell_size - 1, edge_pos[1]), (edge_pos[0] + self.cell_size - 1, edge_pos[1] + self.cell_size - 1), 1)
                            elif edge == 'bottom':
                                pygame.draw.line(screen, cell_color, (edge_pos[0], edge_pos[1] + self.cell_size - 1), (edge_pos[0] + self.cell_size - 1, edge_pos[1] + self.cell_size - 1), 1)
                            elif edge == 'left':
                                pygame.draw.line(screen, cell_color, edge_pos, (edge_pos[0], edge_pos[1] + self.cell_size - 1), 1)

    def get_claimed_cells(self):
        return [cell for cell in self.cells if cell.claimed]
    
    def get_clump(self, cell):
        for representative, clump in self.clump_cache.items():
            if cell in clump and cell.claimed:  # Check if the cell is claimed
                return clump

        visited = set()

        def dfs(current_cell):
            visited.add(current_cell)
            for neighbor in self.get_neighbors(current_cell):
                if neighbor not in visited and neighbor.claimed:
                    dfs(neighbor)

        dfs(cell)
        self.clump_cache[cell] = visited
        return visited if cell.claimed else None  # Return None if the cell is not claimed

    def invalidate_clump_cache(self, cell=None): # remember to invoke this method when a territory expands
        if cell:
            for representative, clump in self.clump_cache.items():
                if cell in clump:
                    del self.clump_cache[representative]
                    return
        else:
            self.clump_cache = {}

    def get_random_cell(self):
        return random.choice(self.cells)