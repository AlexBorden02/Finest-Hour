
import pygame


from ui.button import Button

class PopupWindow:
    def __init__(self, game_state_manager, x, y, width, height, content=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))  # Create a surface for the popup window
        self.content = content
        self.game_state_manager = game_state_manager
        self.buttons = [
            Button("", width - 20, 0, 20, 10, (255, 0, 0), callback=self.close),
        ]
        self.dragging = False
        self.drag_offset = (0, 0)
    
    def close(self, *args):
        self.game_state_manager.ui_manager.remove_popup_window(self)
        self.game_state_manager.ui_manager.set_selected_window(None)

    def render(self, screen):
        # Render the window background
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.rect.width, self.rect.height))

        # Render the content
        if self.content:
            font = pygame.font.Font(None, 36)
            text = font.render(self.content, True, (0, 0, 0))
            self.surface.blit(text, (self.rect.width / 2 - text.get_width() / 2, 20))

        # Render the buttons
        for button in self.buttons:
            button.render(self.surface)
            # update button position
            button.rect.x = button.x
            button.rect.y = button.y

        # Blit the popup window's surface onto the screen at the popup window's position
        screen.blit(self.surface, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print('clicked popup window')
                # Adjust the mouse click position to be relative to the popup window's surface
                local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
                for button in self.buttons:
                    if button.handle_event(pygame.event.Event(event.type, pos=local_pos)):
                        return True
                self.game_state_manager.ui_manager.set_selected_window(self)
                # if click was in top 15 pixels, start dragging
                if event.pos[1] < self.rect.y + 15:
                    self.dragging = True
                    self.drag_offset = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
                return True
        elif self.game_state_manager.ui_manager.get_selected_window() == self: # if this window is selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # if click was in top 15 pixels, start dragging
                    if event.pos[1] < self.rect.y + 15:
                        self.dragging = True
                        self.drag_offset = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
                    return True
                else:
                    self.game_state_manager.ui_manager.set_selected_window(None)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    dx = event.pos[0] - self.drag_offset[0]
                    dy = event.pos[1] - self.drag_offset[1]
                    self.rect.x = dx
                    self.rect.y = dy

                    # Don't update the button's position here
                    # The button's position is relative to the popup window's surface, not the global screen

                    return True
                if self.rect.collidepoint(event.pos):
                    return True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
                return False

    def add_button(self, button):
        self.buttons.append(button)        
        