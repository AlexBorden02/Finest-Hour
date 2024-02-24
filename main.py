import pygame
from settings import hidden_variables as settings

from gameStateManager import GameStateManager
from grid.grid import Grid

# Initialize Pygame
pygame.init()
map_italy = pygame.image.load('map_upscaled.png')

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

cell_size = settings['cell_size']
grid = Grid(map_italy.get_rect().width, map_italy.get_rect().height, cell_size)

# Basic setup for menu and game states
game_state_manager = GameStateManager(grid=grid)
print(game_state_manager.get_state())  # Access current state

def color_in_band(color1, color2, band_factor):
    return all(abs(c1 - c2) <= band_factor for c1, c2 in zip(color1, color2))

# Colors
WATER = (235, 235, 235)  # Blue
LAND = (35, 226, 84)  # Green
SHORELINE = (0, 0, 0)  # Black

# Band factor
band_factor = 10  # Adjust this value to control the color band

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
            if color_in_band(color, WATER, band_factor):
                cell.increment_makeup('water')
            elif color_in_band(color, LAND, band_factor):
                cell.increment_makeup('land')
            elif color_in_band(color, SHORELINE, band_factor):
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
    camera = game_state_manager.ui_manager.get_camera()
    events = pygame.event.get()
    screen.fill((255, 255, 255))

    game_state_manager.run(screen, game_state_manager, camera, events, grid, map_italy, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    pygame.display.flip()