
import pygame
import sys
from ui.button import Button

BLUE = (106, 159, 181)

def main_menu(screen, game_state_manager):
    buttons = [
        Button('New Game', 100, 100, 200, 50, BLUE, game_state_manager.set_state, 'game'),
        Button('Load Game', 100, 200, 200, 50, BLUE),
        Button('Settings', 100, 300, 200, 50, BLUE),
        Button('Quit', 100, 400, 200, 50, BLUE)
    ]
    for button in buttons:
        button.render(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                button.handle_event(event)