
import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, callback=None, callback_args=(), image=None, parent=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.callback = callback  # Function to call when the button is clicked
        self.callback_args = callback_args
        self.image = image
        self.parent = parent  # The element that this button is part of, if any

    def render(self, screen):
            if self.parent:
                # If the button is part of an element, adjust the coordinates and draw onto the element's surface
                rect = pygame.Rect(self.x - self.parent.x, self.y - self.parent.y, self.width, self.height)
                surface = self.parent.surface
            else:
                # If the button is not part of an element, use the original coordinates and draw onto the screen
                rect = self.rect
                surface = screen
            pygame.draw.rect(surface, self.color, rect)
            if self.image:
                surface.blit(self.image, (rect.x, rect.y))
            else:
                font = pygame.font.Font(None, 36)
                text = font.render(self.text, True, (0, 0, 0))
                surface.blit(text, (rect.x + (rect.width / 2 - text.get_width() / 2), rect.y + (rect.height / 2 - text.get_height() / 2)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("Button clicked")
                if self.callback:
                    self.callback(*self.callback_args)
                return True