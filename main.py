import pygame
from settings import hidden_variables as settings

from gameStateManager import GameStateManager
from grid.grid import Grid

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Basic setup for menu and game states
game_state_manager = GameStateManager()
print(game_state_manager.get_state())  # Access current state

# Main game loop
while True:
    game_state = game_state_manager.get_state()
    camera = game_state_manager.ui_manager.get_camera()
    events = pygame.event.get()
    screen.fill((255, 255, 255))

    game_state_manager.run(screen, game_state_manager, camera, events, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    pygame.display.flip()