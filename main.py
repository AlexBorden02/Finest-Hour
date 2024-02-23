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
map_italy = pygame.image.load('map_italy.svg')

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
    
    pygame.display.flip()
