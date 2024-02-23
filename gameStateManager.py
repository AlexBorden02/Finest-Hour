
class GameStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameStateManager, cls).__new__(cls)
            # Initial game state
            cls._instance.state = 'main_menu'
            cls._instance.mouse_down_pos = None

        return cls._instance

    def get_state(self):
        return self._instance.state

    def set_state(self, new_state):
        self._instance.state = new_state
        print(f"Game state changed to: {self._instance.state}")
        return self._instance.state
    
    def get_mouse_down_pos(self):
        return self._instance.mouse_down_pos
    
    def set_mouse_down_pos(self, pos):
        self._instance.mouse_down_pos = pos
        return self._instance.mouse_down_pos

