
from ui_manager import UIManager

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

