
import pygame
from ui.camera import Camera

class UIManager:
    _instance = None

    def __new__(cls, game_state_manager=None):
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance.game_state_manager = game_state_manager
            cls._instance.selected_cell = None
            cls._instance.mouse_down_pos = None
            cls._instance.popup_windows = []
            cls._instance.buttons = []
            cls._instance.camera = Camera(init_pos=(800, 1400), zoom=3, border=pygame.Rect(-1600, -900, 3200, 1800))
        return cls._instance
    
    def update(self, events):
        for event in events:
            self._instance.camera.handle_event(event)

            for window in self._instance.popup_windows:
                window.handle_event(event)

            for button in self._instance.buttons:
                button.handle_event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._instance.game_state_manager.set_state('main_menu')
                    
            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    self._instance.set_mouse_down_pos(event.pos)
            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # left click
                if event.button == 1:
                    window_pos = event.pos
                    if self._instance.get_mouse_down_pos() == window_pos:
                        cell = self._instance.game_state_manager.grid.get_cell(window_pos, self.get_camera())
                        if cell:
                            currently_selected = self._instance.get_selected_cell()
                            if cell == currently_selected:
                                self._instance.set_selected_cell(None)
                            else:
                                self._instance.set_selected_cell(cell)

    def get_camera(self):
        return self._instance.camera
    
    def get_selected_cell(self):
        return self._instance.selected_cell
    
    def set_selected_cell(self, cell):
        self._instance.selected_cell = cell
        return self._instance.selected_cell
    
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

    
    
    