import pygame
import sys
import math

from gameStateManager import GameStateManager
from states.main_menu import main_menu
from states.game import game_interface
from grid.grid import Grid
from ui.camera import Camera

# Initialize Pygame
pygame.init()
map_italy = pygame.image.load('map_italy.png')

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Basic setup for menu and game states
game_state_manager = GameStateManager()
print(game_state_manager.get_state())  # Access current state

camera = Camera(init_pos=(800, 1400), zoom=3, border=pygame.Rect(-1600, -900, 3200, 1800))

cell_size = math.floor(map_italy.get_rect().width / 100)
grid = Grid(map_italy.get_rect().width, map_italy.get_rect().height, cell_size)

# Colors
WATER = (0, 168, 243)  # Blue
LAND = (14, 209, 69)  # Green
SHORELINE = (0, 0, 0)  # Black

# Loop through each cell in the grid
for cell in grid.cells:
    # Loop through each pixel in the cell
    for x in range(cell.id[0]*cell_size, (cell.id[0]+1)*cell_size):
        for y in range(cell.id[1]*cell_size, (cell.id[1]+1)*cell_size):
            try:
                # Get the color of the pixel
                color = map_italy.get_at((x, y))
            except IndexError:
                continue

            # Increment the count of this color in the cell
            if color == WATER:
                cell.increment_makeup('water')
            elif color == LAND:
                cell.increment_makeup('land')
            elif color == SHORELINE:
                cell.increment_makeup('shoreline')

    # once the cell has been analyzed, set the type
    if cell.cell_makeup['shoreline'] > 0:
        cell.set_type('shoreline')
    elif cell.cell_makeup['water'] > cell.cell_makeup['land']:
        cell.set_type('water')
    else:
        cell.set_type('land')

# Main game loop
while True:
    game_state = game_state_manager.get_state()
    events = pygame.event.get()
    
    for event in events:
        camera.handle_event(event) 
            
    screen.fill(WHITE)

    if game_state_manager.get_state() == 'main_menu':
        main_menu(screen, game_state_manager)
    elif game_state_manager.get_state() == 'game':
        game_interface(screen, game_state_manager, camera, events, grid, map_italy, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT)
        game_state_manager.render_popup_windows(screen)
    
    pygame.display.flip()
