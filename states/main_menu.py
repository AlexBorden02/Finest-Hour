
import pygame
import sys
from ui.button import Button

BLUE = (106, 159, 181)

def main_menu(screen, game_state_manager):
    buttons = [
        Button('New Game', 100, 100, 200, 50, BLUE),
        Button('Load Game', 100, 200, 200, 50, BLUE),
        Button('Settings', 100, 300, 200, 50, BLUE),
        Button('Quit', 100, 400, 200, 50, BLUE)
    ]
    for button in buttons:
        button.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    if button.text == 'New Game':
                        print("Game started!")
                        game_state_manager.set_state('game')
                    elif button.text == 'Quit':
                        pygame.quit()
                        sys.exit()