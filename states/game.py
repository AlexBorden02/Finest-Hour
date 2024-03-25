
import pygame
import sys
import memory_profiler 

sys.path.append('..')
from ui.popup import PopupWindow
from ui.button import Button
from ui.element import Element

def expand_territory(game_state_manager):
    selected_cell = game_state_manager.ui_manager.get_selected_cell()
    if selected_cell is not None and selected_cell.get_owner() is not None:
        if selected_cell.get_owner() == game_state_manager.player.get_player_id():
            return game_state_manager.player.claim_cells(game_state_manager.grid.get_random_expansion_cells(game_state_manager.player.claimed_cells, 5, "land"))
        else:
            # must be an npc
            # find the npc that owns the cell
            for npc in game_state_manager.npcs:
                if selected_cell.get_owner() == npc.get_computer_id():
                    return npc.claim_cells(game_state_manager.grid.get_random_expansion_cells(npc.claimed_cells, 5, "land"))
                
class GameInterface:
    def __init__(self, game_state_manager, world_map):
        self.screen = pygame.display.get_surface()
        self.game_state_manager = game_state_manager
        self.camera = game_state_manager.ui_manager.get_camera()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.world_map = world_map

        self.left_toolbar = Element(0, 100, 50, 720-200, (200, 200, 200))

        self.left_toolbar.add_button(Button("save", 10, 110, 30, 30, (100, 100, 100), callback=self.game_state_manager.save_game, callback_args="save1", parent=self.left_toolbar))
        self.left_toolbar.add_button(Button("RL", 10, 150, 30, 30, (100, 100, 100), 
            callback=lambda _: game_state_manager.ui_manager.set_selected_cell(game_state_manager.grid.get_random_cell(cell_type="land")), 
            parent=self.left_toolbar))
        self.left_toolbar.add_button(Button("CT", 10, 190, 30, 30, (100, 100, 100), 
            callback=lambda _: self.game_state_manager.grid.create_territory([self.game_state_manager.ui_manager.get_selected_cell()], self.game_state_manager.player), 
            parent=self.left_toolbar))
        self.left_toolbar.add_button(Button("ET", 10, 230, 30, 30, (100, 100, 100),
            callback=lambda _: self.game_state_manager.ui_manager.get_selected_territory().expand(self.game_state_manager.grid.get_expansion_cells(self.game_state_manager.ui_manager.get_selected_territory(), 5)),
            parent=self.left_toolbar))
        
        self.game_state_manager.ui_manager.add_element(self.left_toolbar)

    def run(self):
        # Calculate the visible portion of the map
        visible_rect = pygame.Rect(-self.camera.offset.x / self.camera.zoom, -self.camera.offset.y / self.camera.zoom, self.SCREEN_WIDTH / self.camera.zoom, self.SCREEN_HEIGHT / self.camera.zoom)
        # Create a new surface that is the size of the visible area
        visible_surface = pygame.Surface((visible_rect.width, visible_rect.height))
        # Fill the new surface with white
        visible_surface.fill((255, 255, 255))

        # Blit the map onto the new surface at the appropriate offset
        visible_surface.blit(self.world_map, (0, 0), visible_rect)

        self.game_state_manager.grid.render(visible_rect, visible_surface, self.camera)

        # Scale the visible surface to the screen size
        scaled_surface = pygame.transform.scale(visible_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # Draw the scaled surface onto the screen
        self.screen.blit(scaled_surface, (0, 0))

        # draw selected cell makeup in top left corner
        font = pygame.font.Font(None, 36)
        if self.game_state_manager.ui_manager.get_selected_cell():
            text = font.render(str(self.game_state_manager.ui_manager.get_selected_cell().__str__()), True, (0, 0, 0))
            self.screen.blit(text, (10, 10))

        #text = font.render(self.game_state_manager.ui_manager.get_selected_cell().get_owner() or None, True, (0, 0, 0))
        #self.screen.blit(text, (10, 50))
