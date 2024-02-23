
class GameStateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameStateManager, cls).__new__(cls)
            # Initial game state
            cls._instance.state = 'main_menu'
            cls._instance.selected_cell = None
            cls._instance.mouse_down_pos = None
            cls._instance.popup_windows = []

        return cls._instance

    def get_state(self):
        return self._instance.state
    
    def get_selected_cell(self):
        return self._instance.selected_cell
    
    def set_selected_cell(self, cell):
        self._instance.selected_cell = cell
        return self._instance.selected_cell

    def set_state(self, new_state):
        self._instance.state = new_state
        print(f"Game state changed to: {self._instance.state}")
        return self._instance.state
    
    def get_mouse_down_pos(self):
        return self._instance.mouse_down_pos
    
    def set_mouse_down_pos(self, pos):
        self._instance.mouse_down_pos = pos
        return self._instance.mouse_down_pos
    
    def add_popup_window(self, window):
        self._instance.popup_windows.append(window)
        return self._instance.popup_windows
    
    def remove_popup_window(self, window):
        self._instance.popup_windows.remove(window)
        return self._instance.popup_windows
    
    def get_popup_windows(self):
        return self._instance.popup_windows
    
    def render_popup_windows(self, screen):
        for window in self._instance.popup_windows:
            window.render(screen)

