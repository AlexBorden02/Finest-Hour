
import pygame
import sys

sys.path.append('..')
from ui.popup import PopupWindow
from ui.button import Button

def game_interface(screen, game_state_manager, camera, events, grid, world_map, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT):
    # Calculate the visible portion of the map
    visible_rect = pygame.Rect(-camera.offset.x / camera.zoom, -camera.offset.y / camera.zoom, SCREEN_WIDTH / camera.zoom, SCREEN_HEIGHT / camera.zoom)
    # Create a new surface that is the size of the visible area
    visible_surface = pygame.Surface((visible_rect.width, visible_rect.height))
    # Fill the new surface with white
    visible_surface.fill((255, 255, 255))

    # Blit the map onto the new surface at the appropriate offset
    visible_surface.blit(world_map, (0, 0), visible_rect)

    # Calculate the position of the circle relative to the map
    circle_pos = (world_map.get_width() // 2 - visible_rect.x, world_map.get_height() // 2 - visible_rect.y)
    # Draw a circle at the calculated position
    pygame.draw.circle(visible_surface, (255, 0, 0), circle_pos, 50)

    # draw selected cell
    selected_cell = game_state_manager.ui_manager.get_selected_cell()
    if selected_cell:
        cell_pos = (selected_cell.rect.x - visible_rect.x, selected_cell.rect.y - visible_rect.y)
        pygame.draw.rect(visible_surface, (0, 255, 0), (cell_pos[0], cell_pos[1], cell_size, cell_size), 1)

    # Scale the visible surface to the screen size
    scaled_surface = pygame.transform.scale(visible_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the scaled surface onto the screen
    screen.blit(scaled_surface, (0, 0))

    buttons = []

    for button in buttons:
        button.render(screen)

    # draw selected cell makeup in top left corner
    if selected_cell:
        font = pygame.font.Font(None, 36)
        text = font.render(str(selected_cell.cell_makeup), True, (0, 0, 0))
        screen.blit(text, (10, 10))

    # simple popup window
    #popupTest = PopupWindow(game_state_manager=game_state_manager, x=100, y=100, width=400, height=200, content="Hello, world!")

    game_state_manager.ui_manager.update(events)
        
