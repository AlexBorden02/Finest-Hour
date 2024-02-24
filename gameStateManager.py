
from ui_manager import UIManager
from states.main_menu import main_menu
from states.game import game_interface

class GameStateManager:
    _instance = None

    def __new__(cls, grid=None):
        if cls._instance is None:
            cls._instance = super(GameStateManager, cls).__new__(cls)
            # Initial game state
            cls._instance.state = 'main_menu'
            cls._instance.ui_manager = UIManager(cls._instance)
            cls._instance.grid = grid

        return cls._instance

    def get_state(self):
        return self._instance.state
    
    def set_state(self, new_state):
        self._instance.state = new_state
        print(f"Game state changed to: {self._instance.state}")
        return self._instance.state
    
    def get_ui_manager(self):
        return self._instance.ui_manager
    
    def get_grid(self):
        return self._instance.grid
    
    def run(self, screen, game_state_manager, camera, events, grid, map_italy, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT):
        if self._instance.state == 'main_menu':
            main_menu(screen, game_state_manager)
        elif self._instance.state == 'game':
            game_interface(screen, game_state_manager, camera, events, grid, map_italy, cell_size, SCREEN_WIDTH, SCREEN_HEIGHT)
            game_state_manager.get_ui_manager().update(events)
            game_state_manager.get_ui_manager().render(screen)
            

