
import pygame
import sys

sys.path.append('..')
from ui.popup import PopupWindow
from ui.button import Button

def game_interface(screen, game_state_manager, camera, events, world_map, SCREEN_WIDTH, SCREEN_HEIGHT):
    # Calculate the visible portion of the map
    visible_rect = pygame.Rect(-camera.offset.x / camera.zoom, -camera.offset.y / camera.zoom, SCREEN_WIDTH / camera.zoom, SCREEN_HEIGHT / camera.zoom)
    # Create a new surface that is the size of the visible area
    visible_surface = pygame.Surface((visible_rect.width, visible_rect.height))
    # Fill the new surface with white
    visible_surface.fill((255, 255, 255))

    # Blit the map onto the new surface at the appropriate offset
    visible_surface.blit(world_map, (0, 0), visible_rect)

    # # Calculate the position of the circle relative to the map
    # circle_pos = (world_map.get_width() // 2 - visible_rect.x, world_map.get_height() // 2 - visible_rect.y)
    # # Draw a circle at the calculated position
    # pygame.draw.circle(visible_surface, (255, 0, 0), circle_pos, 50)

    # draw selected cell
    selected_cell = game_state_manager.ui_manager.get_selected_cell()
    if selected_cell:
        cell_pos = (selected_cell.rect.x - visible_rect.x, selected_cell.rect.y - visible_rect.y)
        pygame.draw.rect(visible_surface, (0, 255, 0), (cell_pos[0], cell_pos[1], game_state_manager.grid.get_cell_size(), game_state_manager.grid.get_cell_size()), 1)

    # Scale the visible surface to the screen size
    scaled_surface = pygame.transform.scale(visible_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the scaled surface onto the screen
    screen.blit(scaled_surface, (0, 0))

    # draw selected cell makeup in top left corner
    font = pygame.font.Font(None, 36)
    if selected_cell:
        text = font.render(str(selected_cell.cell_makeup), True, (0, 0, 0))
        screen.blit(text, (10, 10))

    isSelected = lambda window: window.selected.__str__()

    text = font.render(game_state_manager.ui_manager.get_selected_window().__str__(), True, (0, 0, 0))
    screen.blit(text, (10, 50))
            
