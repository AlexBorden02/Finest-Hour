
import pygame
from ui.camera import Camera
from ui.popup import PopupWindow
from ui.button import Button


class UIManager:
    _instance = None

    def __new__(cls, game_state_manager=None):
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance.game_state_manager = game_state_manager
            cls._instance.selected_cell = None
            cls._instance.selected_window = None
            cls._instance.selected_clump = None
            cls._instance.mouse_down_pos = None
            cls._instance.popup_windows = []
            cls._instance.buttons = []
            cls._instance.elements = []
            cls._instance.camera = Camera(zoom=3, max_zoom=3, min_zoom=1)
        return cls._instance
        
    
    def update(self, events):
        testPopup = PopupWindow(self._instance.game_state_manager, 400, 400, 200, 200, "test")
        testPopup.add_button(Button("test", 50, 50, 50, 50, (255, 0, 0)))

        for event in events:
            window_interaction = any(window.handle_event(event) for window in self._instance.popup_windows)
            button_interaction = any(button.handle_event(event) for button in self._instance.buttons)
            element_interaction = any(element.handle_event(event) for element in self._instance.elements)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pauseMenu = PopupWindow(self._instance.game_state_manager, 500, 200, 200, 500)
                    pauseMenu.add_button(Button("Main menu", 50, 250, 100, 50, (255, 0, 0), self._instance.game_state_manager.set_state, 'main_menu'))
                    self._instance.add_popup_window(pauseMenu)
                if event.key == pygame.K_m:
                    self._instance.add_popup_window(testPopup)
                if event.key == pygame.K_e:
                    self._instance.game_state_manager.npcs[0].claim_cell(self._instance.selected_cell)
                # if ctrl + s is pressed, save the game
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self._instance.game_state_manager.save_game("save1")
            # essentially just checking if the mouse is not interacting with a window or button
            # if it is not, then the camera should handle the event
            if not window_interaction and not button_interaction and not element_interaction:
                self._instance.camera.handle_event(event)
                    
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
                    elif event.button == 3: # right click
                        window_pos = event.pos
                        cell = self._instance.game_state_manager.grid.get_cell(window_pos, self.get_camera())
                        if cell:
                            if cell.claimed:
                                self._instance.game_state_manager.player.unclaim_cell(cell)
                            else:
                                self._instance.game_state_manager.player.claim_cell(cell)
                 

    def get_camera(self):
        return self._instance.camera
    
    def get_selected_cell(self):
        return self._instance.selected_cell
    
    def set_selected_cell(self, cell):
        self._instance.selected_cell = cell
        if cell is not None:
            self._instance.selected_clump = self._instance.game_state_manager.grid.get_clump(cell)
        else:
            self._instance.selected_clump = None
        return self._instance.selected_cell
    
    def get_selected_window(self):
        return self._instance.selected_window
    
    def set_selected_window(self, window):
        self._instance.selected_window = window
        return self._instance.selected_window
    
    def get_selected_clump(self):
        return self._instance.selected_clump
    
    def set_selected_clump(self, clump):
        self._instance.selected_clump = clump
        return self._instance.selected_clump
    
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

    def add_button(self, button):
        self._instance.buttons.append(button)
        return self._instance.buttons
    
    def remove_button(self, button):
        self._instance.buttons.remove(button)
        return self._instance.buttons
    
    def get_buttons(self):
        return self._instance.buttons
    
    def render_buttons(self, screen):
        for button in self._instance.buttons:
            button.render(screen)

    def render_elements(self, screen):
        for element in self._instance.elements:
            element.render(screen)

    def render(self, screen):
        self._instance.render_elements(screen)
        self._instance.render_popup_windows(screen)
        self._instance.render_buttons(screen)

    def add_element(self, element):
        self._instance.elements.append(element)
        return self._instance.elements

    
    
    