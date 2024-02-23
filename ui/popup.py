
import pygame


from ui.button import Button

class PopupWindow:
    def __init__(self, game_state_manager, x, y, width, height, content=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.content = content  # This could be text or images
        self.visible = True  # Initially visible
        self.game_state_manager = game_state_manager
        self.buttons = [
            Button("", x + width - 20, y, 20, 10, (255, 0, 0), callback=self.close),
        ]
        self.dragging = False  # Initially not dragging
        self.drag_offset = (0, 0)  # Initially no offset
    

    def show(self, *args):
        self.visible = True

    def hide(self, *args):
        self.visible = False
    
    def close(self, *args):
        self.game_state_manager.remove_popup_window(self)

    def render(self, screen):
        if self.visible:
            # Render the window background
            pygame.draw.rect(screen, (200, 200, 200), self.rect)
            
            # Render the content
            if self.content:
                font = pygame.font.Font(None, 36)
                text = font.render(self.content, True, (0, 0, 0))
                screen.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2), self.rect.y + 20))

            # Render the buttons
            for button in self.buttons:
                button.render(screen)

    def handle_event(self, event):
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                return button.callback(button.callback_args)
